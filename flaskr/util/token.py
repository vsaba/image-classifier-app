from itsdangerous import URLSafeTimedSerializer, BadSignature
from flask import current_app


def generate_token(email):
    """
    Generates a token from the provided params

    :param email: The provided value to be encoded
    :return: The token of the encoded value
    """
    serializer = URLSafeTimedSerializer(secret_key=current_app.config['SECRET_KEY'],
                                        salt=current_app.config['TOKEN_SERIALIZER_SALT'])
    return serializer.dumps(email)


def verify_token(token, max_age=600):
    """
    Verifies the provided token

    :param token: The provided token
    :param max_age: The maximum age of the validity of the token, default is 10 minutes
    :return: The decoded value if decoding is successful, False otherwise
    """
    serializer = URLSafeTimedSerializer(secret_key=current_app.config['SECRET_KEY'],
                                        salt=current_app.config['TOKEN_SERIALIZER_SALT'])
    try:
        user_id = serializer.loads(token, max_age=max_age)
        return user_id
    except BadSignature:
        pass

    return False
