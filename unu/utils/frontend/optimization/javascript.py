import os
import logging


import slimit


import unu


logger = logging.getLogger(__name__)


def update_file(file_name):
	unu.utils.frontend.optimization.common.update_file(file_name, 'js', minify)


def optimize(js):
	return slimit.minify(js, mangle=True, mangle_toplevel=False), True


def minify(js):
	return os.linesep.join(
		[
			s for s in
			'\'use strict\';{}'.format(js.replace('"use strict";', '').replace('\'use strict\';', '')).splitlines()
			if s.strip() != ''
		]
	)
