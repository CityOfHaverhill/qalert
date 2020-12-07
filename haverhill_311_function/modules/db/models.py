from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Float, VARCHAR, Text
from sqlalchemy.orm import validates
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape
from geoalchemy2.types import WKBElement
from shapely.geometry import Point

NAD_83 = 4269
Base = declarative_base()


def construct_point(context) -> WKBElement:
    latitude = context.get_current_parameters()['latitude']
    longitude = context.get_current_parameters()['longitude']
    return from_shape(
        shape=Point(longitude, latitude),
        srid=NAD_83
    )


class QAlertRequest(Base):
    """Sqlalchemy orm model for the qalert requests table"""
    __tablename__ = 'qalert_requests'
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    create_date = Column(DateTime)
    create_date_unix = Column(Integer)
    last_action = Column(DateTime)
    last_action_unix = Column(Integer)
    type_id = Column(Integer)
    type_name = Column(VARCHAR(length=200))
    comments = Column(VARCHAR(length=5000))
    street_num = Column(VARCHAR(length=100))
    street_name = Column(VARCHAR(length=100))
    cross_name = Column(VARCHAR(length=100))
    city_name = Column(VARCHAR(length=100))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    point = Column(
        Geometry(
            geometry_type='POINT',
            srid=NAD_83
        ),
        nullable=False,
        default=construct_point
    )

    @validates('type_name', 'comments', 'street_num', 'street_name', 'cross_name', 'city_name')  # noqa: E501
    def validate_length(self, key, value):
        max_len = getattr(self.__class__, key).prop.columns[0].type.length
        if len(value) > max_len:
            return value[:max_len]
        return value


class QAlertAudit(Base):
    """Sqlalchemy orm model for the qalert audit table"""
    __tablename__ = 'qalert_audits'
    id = Column(Integer, primary_key=True)
    create_date = Column(Text)
