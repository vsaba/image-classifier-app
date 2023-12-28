from itsdangerous import URLSafeTimedSerializer, BadTimeSignature
from flask import current_app


def generate_token(user_id):
    serializer = URLSafeTimedSerializer(secret_key=current_app.config['SECRET_KEY'],
                                        salt=current_app.config['TOKEN_SERIALIZER_SALT'])
    return serializer.dumps(user_id)


def verify_token(token, max_age=600):
    serializer = URLSafeTimedSerializer(secret_key=current_app.config['SECRET_KEY'],
                                        salt=current_app.config['TOKEN_SERIALIZER_SALT'])
    try:
        user_id = serializer.loads(token, max_age=max_age)
        return user_id
    except BadTimeSignature:
        pass

    return False
