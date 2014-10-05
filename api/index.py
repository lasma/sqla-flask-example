from flask.ext.restful import Resource

class IndexApi(Resource):

    def get(self):

        return "hello!"