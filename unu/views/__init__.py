from . import add_closure_compiler
from . import analyze
from . import fiu
from . import fiu_app
from . import fiu_get_files
from . import fiu_new_app
from . import fiu_new_component
from . import fiu_new_page
from . import fix_js_namespaces
from . import fix_models
from . import fix_urls
from . import fix_views
from . import get_apps
from . import get_models
from . import get_urls
from . import index
from . import new_view
from . import new_view_create
from . import optimize_client_code
from . import toggle_template_static


__all__ = [
	'add_closure_compiler',
	'analyze',
	'fiu',
	'fiu_app',
	'fiu_get_files',
	'fiu_new_app',
	'fiu_new_component',
	'fiu_new_page',
	'fix_js_namespaces',
	'fix_models',
	'fix_urls',
	'fix_views',
	'get_apps',
	'get_models',
	'get_urls',
	'index',
	'new_view',
	'new_view_create',
	'optimize_client_code',
	'toggle_template_static',
]
