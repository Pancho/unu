import datetime
import logging


import jwt
from django.conf import settings
from django.utils import timezone


logger = logging.getLogger(__name__)


def decode(request):
	return decode_token(request.headers.get('Authentication'))


def decode_token(token):
	return jwt.decode(token.replace('JWTToken ', ''), settings.SECRET_KEY, algorithms=['HS256'])


def encode(user_id, expire_seconds=3600):
	return jwt.encode({
		'id': user_id,
		'exp': (timezone.now() + datetime.timedelta(seconds=expire_seconds))
	}, settings.SECRET_KEY, 'HS256').decode('utf-8')
