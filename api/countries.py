from flask.ext.restful import Resource
from config import Session
from model import Countries
from common.exception import ExceptionHandler

class CountriesApi(Resource):

    @ExceptionHandler
    def get(self):

        session = Session()
        records = session.query(Countries).all()

        countries = [record.get_as_dict() for record in records]

        response = dict(data=countries)

        return response, 200