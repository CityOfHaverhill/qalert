"""The sanitizer module cleans and processes 311 data retreived from QAlert
    in preperation for storage in db.
"""

def sanitize(data):
    
    """ Clean is a list of keys that need to be deleted """

    clean = ["createDateUnix", "id", "priorityToDisplay", "status", "lastAction", "lastActionUnix", "hasLinks", "streetNum", "streetName", "crossName", "cityName", "name", "email" ]
    for dictionary in data: 
        for j in clean: 
            dictionary.pop(j)
    return data


