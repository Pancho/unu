import os
import logging

from calmjs.parse import es5
from calmjs.parse.unparsers.es5 import minify_print

import unu


logger = logging.getLogger(__name__)


def update_file(file_name):
    unu.utils.frontend.optimization.common.update_file(file_name, "js", minify)


def optimize(js_content):
    return (
        minify_print(es5(js_content), obfuscate=True, obfuscate_globals=False),
        True,
    )


def minify(js_content):
    return os.linesep.join(
        [
            s
            for s in f"'use strict';"
            f"""{
                     js_content
                     .replace('"use strict";', "")
                     .replace("'use strict';", "")
                }""".splitlines()
            if s.strip() != ""
        ]
    )
