from flask.ext.restful import Resource
from config import Session
from model import Cities

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