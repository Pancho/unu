import json
import decimal
import datetime

from bson import objectid
from django.utils.timezone import is_aware


class Encoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, ObjectID and
    decimal types.
    """

    def default(self, o):
        result = None
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            date_time = o.isoformat()
            if o.microsecond:
                date_time = date_time[:23] + date_time[26:]
            if date_time.endswith("+00:00"):
                date_time = date_time[:-6] + "Z"
            result = date_time
        elif isinstance(o, objectid.ObjectId):
            result = str(o)
        elif isinstance(o, datetime.date):
            result = o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            date_time = o.isoformat()
            if o.microsecond:
                date_time = date_time[:12]
            result = date_time
        elif isinstance(o, decimal.Decimal):
            result = str(o)
        elif isinstance(o, set):
            result = list(o)
        else:
            result = json.JSONEncoder.default(self, o)

        return result
