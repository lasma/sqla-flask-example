from flask.ext.restful import Resource
from config import Session
from model import Cities
from common.exception_handler import ExceptionHandler

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

    @ExceptionHandler
    def get(self, id):

        session = Session()
        city = session.query(Cities).get(id)
        if city:
            response = dict(data=city.get_as_dict())
        else:
            return "city with id={} does not exist!".format(id), 400

        return response, 200