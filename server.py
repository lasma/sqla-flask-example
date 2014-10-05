from flask import Flask

from flask.ext.restful import Api
from api import IndexApi, RoadsApi


app = Flask(__name__)
app.config['DEBUG'] = True

api = Api(app)
api.add_resource(RoadsApi, '/', '/api/roads')
api.add_resource(IndexApi, '/', '/index')

if __name__ == "__main__":
    print "App is running!"
    app.run()


