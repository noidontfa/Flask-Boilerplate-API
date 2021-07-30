# FLASK BOILERPLATE API PROJECT

## Pre-commit
```
pre-commit install
pre-commit run --all-files
```

## Flask Migration
```
flask db init
flask db migrate
flask db upgrade
flask db downgrade
```

## Usage
```
core_bp = Blueprint("core", __name__, url_prefix="")
core_api = CoreAPI(core_bp)

core_api.add_resource(TestResource, "/")

class TestResource(AuthenticateResource):
    def get(self, *args, **kwargs):
        return {"hello": "world"}

class TestResource(AllowAnyResource):
    def get(self, *args, **kwargs):
        return {"hello": "world"}

```