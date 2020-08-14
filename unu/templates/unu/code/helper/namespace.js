{% for include in js_includes %}// include:media/js/{{ include }}
{% endfor %}'use strict';

{% if is_js_root %}var {% endif %}{{ js_namespace }} = {};
