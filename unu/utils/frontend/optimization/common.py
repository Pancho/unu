import os
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def deduplicate_list(seq):
    seen = set()
    seen_add = seen.add
    return [item for item in seq if not (item in seen or seen_add(item))]
