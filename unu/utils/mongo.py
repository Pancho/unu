import logging
import re

import pymongo
from bson import code
from django.conf import settings


ASC = pymongo.ASCENDING
DSC = pymongo.DESCENDING


logger = logging.getLogger(__name__)
db = pymongo.MongoClient(
    (
        f"mongodb://{settings.MONGO_DB_USERNAME}"
        f":{settings.MONGO_DB_PASSWORD}"
        f"@{settings.MONGO_DB_ENDPOINT_URL}"
        f":{settings.MONGO_DB_ENDPOINT_PORT}"
    )
)


def get_map_reduce(name):
    with open(f"utils/mongojs/{name}/map.js", "r", encoding="utf-8") as map_file:
        map_js = code.Code(re.sub(r"^\(|\);$|\)$", "", map_file.read()))

    with open(f"utils/mongojs/{name}/reduce.js", "r", encoding="utf-8") as reduce_file:
        reduce_js = code.Code(re.sub(r"^\(|\);$|\)$", "", reduce_file.read()))

    # Use this as *args for map_reduce method on collection
    return map_js, reduce_js, name
