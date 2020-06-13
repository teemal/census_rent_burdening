import os

class Census(object):
    def __init__(self):
        pass

    def get_census_api_key(self):
        if(os.environ['FLASK_ENV'] == 'dev'):
            return os.getenv('CENSUS_API_KEY')
        else:
            return os.environ['CENSUS_API_KEY']

    