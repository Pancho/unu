import logging


from Crypto import Random
from Crypto.Cipher import AES


logger = logging.getLogger(__name__)


def pad(text):
	return text + b'\0' * (AES.block_size - len(text) % AES.block_size)


def encrypt(message, key):
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	message = pad(message)
	return iv + cipher.encrypt(message)


def decrypt(cipher_text, key):
	iv = cipher_text[:AES.block_size]
	cipher = AES.new(key, AES.MODE_CBC, iv)
	plain_text = cipher.decrypt(cipher_text[AES.block_size:])
	return plain_text.rstrip(b'\0')
