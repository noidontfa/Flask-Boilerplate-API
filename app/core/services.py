from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)


class CoreService:
    @classmethod
    def generate_user_token(cls, user_id):
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return dict(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    def get_user_identity(cls, refresh=False):
        @jwt_required(refresh=refresh)
        def identify():
            return get_jwt_identity()

        user_id = identify()
        return user_id
