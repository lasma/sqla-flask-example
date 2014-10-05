from flask.ext.restful import Resource

class RoadsApi(Resource):

    def get(self):
        """Example of static data return - it's easy to return hard coded data."""

        road = dict()
        road["name"] = "Abbott"
        road["feature"] = {"geometry": {"type": "LineString", "coordinates": [[102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]]}}

        roads = dict()
        roads["roads"] = [road]

        return roads