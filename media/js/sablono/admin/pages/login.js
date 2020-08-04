import { BoxComponent } from '../../components/box.js';
import { FieldComponent } from '../../components/field.js';
import { FormComponent } from '../../components/form.js';
import { GridComponent } from '../../components/grid.js';
import { Component } from '../../fiu/component.js';

export class LoginPageComponent extends Component {
	static tagName = 'login-page';
	static template = 'components/login-page';
	static stylesheets = [
		'meta',
		'palette',
		'font-awesome',
		'normalize',
		'main',
		'components/login-page',
	];
	static registerComponents = [
		BoxComponent,
		GridComponent,
		FormComponent,
		FieldComponent,
	];

	constructor() {
		super(LoginPageComponent);
		console.log('LoginPageComponent constructor finished');
	}

	onTemplateLoaded() {
		const header = document.querySelector('sablono-header'),
			form = this.shadowRoot.querySelector('sablono-form');
		form.setSuccessHandler(response => {
			if (response.status === 'ok') {
				window.localStorage.setItem('auth-token', response.token);
				this.app.router.navigate(window.location.hash.replace('#', ''));
				header.setAttribute('authenticated', 'authenticated');
			} else {
				header.setAttribute('authenticated', '');
				form.setErrors(response.errors);
			}
		});
	}

	populateFields() {
		return {};
	}
}
