from flask.ext.restful import Resource
from config import Session
from model import Cities
from common.exception.handler import ExceptionHandler
from common.httpcodes import *

class CitiesApi(Resource):

    def get(self):

        session = Session()
        records = session.query(Cities).all()

        cities = list()
        for record in records:
            city = dict()
            city["id"] = record.gid
            city["name"] = record.name
            cities.append(city)

        response = dict(data=cities)

        return response, 200


class CitiesIdApi(Resource):

    # Wrap get call in ExceptionHandler to gracefully recover from unexpected api errors
    # Easy way to see ExceptionHandler at work is to call http://localhost:5000/api/cities/a
    @ExceptionHandler
    def get(self, id):
        """Get city by ID and return as unique resource.

        For example:
            http://localhost:5000/api/cities/1

        :param id {int}: unique id of the city to return
        :return:
        """

        session = Session()
        city = session.query(Cities).get(id)
        if city:
            response = dict(data=city.get_as_dict())
        else:
            return "City with id={} does not exist!".format(id), HTTP_NOT_FOUND_CODE

        return response, HTTP_OK_CODE