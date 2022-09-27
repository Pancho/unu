import App from '../fiu/js/app.js';

new App({
	routeRoot: '{{ router_root_url }}',
	staticRoot: '{{ static_root_url }}',
	homePage: {
		component: {{ index_page }},
	},
	notFound: {
		component: {{ not_found_page }},
	},
	routes: [{% for route in routes %}
		{
			path: '{{ route.path }}',
			component: {{ route.class_name }},{% if route.guard %}
			guard: {{ route.guard }},{% endif %}{% if route.hooks %}
			hooks: {{ route.hooks|safe }},{% endif %}
		},{% endfor %}
	],{% if authentication_url %}
	authenticationUrl: '{{ authentication_url }}',{% endif %}
	authenticationModule: {% if authentication_module %}{{ authentication_module }}{% else %}null{% endif %},
	providers: [{% for provider in providers %}
		{{ provider }},{% endfor %}
	],
	rootComponents: [
		{{ index_page }},
		{{ not_found_page }},{% for route in routes %}
		{{ route.class_name }},{% endfor %}
	],
	rootStylesheets: [{% for stylesheet_path in root_stylesheets %}
		'{{ stylesheet_path }}',{% endfor %}
	],
	httpEndpointStub: '{{ http_endpoint_stub }}',
	onAppReady: [{% if on_app_ready %}
		{{ on_app_ready|safe }}{% endif %}
	],
	loggerConfig: {% if logger_config %}{
		{{ logger_config|safe }}
	}{% else %}null{% endif %},
});
