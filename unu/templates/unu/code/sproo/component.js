import Component from '{{ static_path }}{{ app }}/js/sproo/js/component.js';{% if provide_store %}
import { takeUntil } from '{{ static_path }}{{ app }}/js/sproo/js/reactive/operators.js';
import { Subject } from '{{ static_path }}{{ app }}/js/sproo/js/reactive/subject.js';{% if component_type == 'pages' %}
import Store from '{{ static_path }}{{ app }}/js/sproo/js/state-management.js';{% endif %}{% endif %}

export default class {{ class_name }} extends Component {
	static tagName = '{{ tag_name }}';
	static template = '{{ static_path }}{{ app }}/js/{{ app_name }}/{{ component_type }}/{{ component_path }}';
	static stylesheets = [
		'{{ static_path }}{{ app }}/js/sproo/css/meta',
		'{{ static_path }}{{ app }}/js/sproo/css/normalize',{% if include_stylesheet %}
		'{{ static_path }}{{ app }}/js/{{ app_name }}/{{ component_type }}/{{ component_path }}',{% endif %}
	];
	static registerComponents = [
	];{% if provide_store %}{% if component_type == 'pages' %}
	static STORE_PROVIDER = [
		{{ class_name }},
		'store',
		{
			useFactory: Store.get,
			params: ['{{ component_type }}/{{ path_stub }}', true],
		},
	];{% endif %}

	unsubscribe = new Subject();{% endif %}

	constructor({{ params }}) {
		super();{% if enable_logging %}
		this.logger.log('{{ class_name }} constructor finished');{% else %}
		console.log('{{ class_name }} constructor finished'){% endif %}{% if provide_store %}
		// this.store.select('slice/part').pipe(
		// 	takeUntil(this.unsubscribe),
		// ).subscribe();{% endif %}
	}

	unload() {{% if provide_store %}
		this.unsubscribe.next();
		this.unsubscribe.complete();{% endif %}
	}

	onTemplateLoaded() {
	}
}
