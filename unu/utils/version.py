import os
import time


STATIC_FILES_VERSION = os.environ.get('APP_VERSION', int(time.time()))
