from jwt import encode, decode
from settings import secret_key
from datetime import datetime, timedelta


def encode_token(**payload):
    try:
        token = encode({**payload,'exp': datetime.utcnow()
                        + timedelta(hours=1)}, secret_key, algorithm='HS256')
        return token
    except Exception as e:
        raise e


def decode_token(token:str):
    try:
        decoded = decode(token, secret_key, algorithms=['HS256'])
        return decoded
    except Exception as e:
        raise e
