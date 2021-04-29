from os import urandom
from hashlib import pbkdf2_hmac

def encode_hash(payload: str):
    salt = urandom(32)
    payload_encoded = payload.encode('utf-8')
    key = pbkdf2_hmac('sha256', payload_encoded, salt, 1000, dklen=128)
    storage = salt + key
    return storage


def decode_hash(payload: str, hash_storage: bytes):
    salt = hash_storage[:32]
    key_storage = hash_storage[32:]
    payload_encoded = payload.encode('utf-8')
    key = pbkdf2_hmac('sha256', payload_encoded, salt, 1000, dklen=128)
    if key.hex() == key_storage.hex():
        return True
    return False