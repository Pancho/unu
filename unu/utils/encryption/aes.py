import logging

from Crypto import Random
from Crypto.Cipher import AES


logger = logging.getLogger(__name__)


def pad(text):
    return text + b"\0" * (AES.block_size - len(text) % AES.block_size)


def encrypt(message, key):
    salt = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, salt)
    message = pad(message)
    return salt + cipher.encrypt(message)


def decrypt(cipher_text, key):
    salt = cipher_text[: AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, salt)
    plain_text = cipher.decrypt(cipher_text[AES.block_size :])
    return plain_text.rstrip(b"\0")
