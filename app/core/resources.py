from flask_restful import Resource

from app.core.middleware import authenticate, wrap_exception


class AuthenticationResource(Resource):
    method_decorators = [wrap_exception, authenticate]


class AllowAnyResource(Resource):
    method_decorators = [wrap_exception]
