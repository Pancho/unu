{% for include in js_includes %}// include:media/js/{{ include }}
{% endfor %}'use strict';

{{ js_namespace }} = (function () {
	var r = {

	}, u = {
		initialize: function () {

		}
	};

	return u;
})();

{{ js_namespace }}.initialize();
