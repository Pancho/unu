import logging


from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA


logger = logging.getLogger(__name__)


def encrypt(message, public_key):
    key = RSA.importKey(public_key)
    cipher = PKCS1_OAEP.new(key)
    encrypted = cipher.encrypt(message)
    return encrypted


def decrypt(encrypted, private_key):
    key = RSA.importKey(private_key)
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(encrypted)
