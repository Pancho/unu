import os
import logging


from calmjs.parse import es5
from calmjs.parse.unparsers.es5 import minify_print


import unu


logger = logging.getLogger(__name__)


def update_file(file_name):
	unu.utils.frontend.optimization.common.update_file(file_name, 'js', minify)


def optimize(js):
	return minify_print(es5(js), obfuscate=True, obfuscate_globals=False), True


def minify(js):
	return os.linesep.join(
		[
			s for s in
			'\'use strict\';{}'.format(js.replace('"use strict";', '').replace('\'use strict\';', '')).splitlines()
			if s.strip() != ''
		]
	)
