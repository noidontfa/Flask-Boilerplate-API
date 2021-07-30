from flask_restful import Resource


class TestResource(Resource):
    def get(self, *args, **kwargs):
        return {"hello": "world"}
