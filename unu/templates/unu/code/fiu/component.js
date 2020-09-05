import { Component } from '../../../fiu/js/component.js';{% if provide_store %}
import { takeUntil } from '../../../fiu/js/reactive/operators.js';
import { Subject } from '../../../fiu/js/reactive/subject.js';{% if component_type == 'pages' %}
import { Store } from '../../../fiu/js/state.js';{% endif %}{% endif %}

export class {{ class_name }} extends Component {
	static tagName = '{{ tag_name }}';
	static template = '/{{ media_path }}{{ app_path }}/{{ component_type }}/{{ component_path }}';
	static stylesheets = [
		'/{{ media_path }}fiu/css/meta',
		'/{{ media_path }}fiu/css/normalize',{% if include_stylesheet %}
		'/{{ media_path }}{{ app_path }}/{{ component_type }}/{{ component_path }}',{% endif %}
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
		super({{ class_name }});{% if enable_logging %}
		this.logger.log('{{ class_name }} constructor finished')();{% else %}
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

	populateFields() {
		return {
		};
	}
}
