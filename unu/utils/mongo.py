import logging
import re


import pymongo
from bson import code
from django.conf import settings


ASC = pymongo.ASCENDING
DSC = pymongo.DESCENDING


logger = logging.getLogger(__name__)
db = pymongo.MongoClient(f'mongodb://{settings.MONGO_DB_USERNAME}:{settings.MONGO_DB_PASSWORD}@{settings.MONGO_DB_ENDPOINT_URL}:{settings.MONGO_DB_ENDPOINT_PORT}')


def get_map_reduce(name):
	with open(f'utils/mongojs/{name}/map.js', 'r') as map_file:
		map_js = code.Code(re.sub(r'^\(|\);$|\)$', '', map_file.read()))

	with open(f'utils/mongojs/{name}/reduce.js', 'r') as reduce_file:
		reduce_js = code.Code(re.sub(r'^\(|\);$|\)$', '', reduce_file.read()))

	# Use this as *args for map_reduce method on collection
	return map_js, reduce_js, name
