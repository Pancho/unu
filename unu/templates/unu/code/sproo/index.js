import App from '{{ static_path }}{{ app }}/js/sproo/js/app.js';

new App({
	routeRoot: '{{ router_root_url }}',
	staticRoot: '{{ static_root_url }}',
	homePage: {
		component: '{{ index_page }}',
	},
	notFound: {
		component: '{{ not_found_page }}',
	},
	routes: [{% for route in routes %}
		{
			path: '{{ route.path }}',
			component: '{{ route.component }}',{% if route.guard %}
			guard: {{ route.guard }},{% endif %}{% if route.hooks %}
			hooks: {{ route.hooks|safe }},{% endif %}
		},{% endfor %}
	],{% if authentication_url %}
	authenticationUrl: '{{ authentication_url }}',{% endif %}{% if authentication_module %}
	authenticationModule: '{{ authentication_module }}',{% endif %}{% if providers %}
	providers: [{% for provider in providers %}
		{{ provider }},{% endfor %}
	],{% endif %}
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
