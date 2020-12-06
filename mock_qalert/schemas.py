from marshmallow import Schema, fields, EXCLUDE, validate


class GetRequestsSchema(Schema):
    """ /api/requests/get - GET

    Parameters:
     - api_key (str)
     - count (int)
     - sort (str)
     - create_date_min (str)
    """
    class Meta:
        unknown = EXCLUDE

    api_key = fields.Str(required=True, data_key='key')
    count = fields.Int(required=False, default=-1)
    sort = fields.Str(
        required=False, 
        default='[createdate] asc',
        validate=validate.Regexp(r"^\[(\D*)\] (asc|desc)(,?)$")
    )
    create_date_min = fields.DateTime(r"%m/%d/%Y %I:%M %p", required=False, data_key='createDateMin')
