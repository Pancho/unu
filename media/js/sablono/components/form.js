import { Component } from '../fiu/component.js';
import { Mavor } from '../fiu/mavor.js';

export class FormComponent extends Component {
	static tagName = 'sablono-form';
	static template = 'components/form';
	static stylesheets = [
		'palette',
		'font-awesome',
		'normalize',
		'components/form',
	];

	form;
	control;
	button;
	errors;

	headers = {};
	requestOptions = {};
	successHandler = response => response;
	parser = response => response.json();

	fieldTranslations;

	constructor() {
		super(FormComponent);
		console.log('FormComponent constructor finished');
	}

	onTemplateLoaded() {
		const submitValue = this.attribute('submit-value'),
			skipAuthentication = this.attribute('skip-authentication');

		if (!!submitValue) {
			this.control.classList.add('show');
			this.button.setAttribute('value', submitValue);
		}

		this.form.addEventListener('submit', (event) => {
			event.preventDefault();

			const formData = new FormData();
			Object.entries(this.compileValues()).forEach((entry, index) => {
				formData.append(...entry);
			});

			if (this.validate()) {
				this.app.http[this.attribute('method')](
					this.attribute('action'),
					formData,
					this.requestOptions,
					this.headers,
					skipAuthentication !== 'true',
				).then(this.parser).then(this.successHandler);
			}
		});
	}

	populateFields() {
		return {
			form: 'form',
			control: 'form fieldset .control',
			button: 'form fieldset .control .button',
			errors: '.errors',
		};
	}

	validate() {
		const fields = this.querySelectorAll('sablono-field');
		let valid = true;
		fields.forEach((field, index) => {
			valid = valid && field.validate();
		});

		return valid;
	}

	compileValues() {
		const result = {},
			fields = this.querySelectorAll('sablono-field');

		fields.forEach((field, index) => {
			Object.assign(result, field.compileValues(this.fieldTranslations));
		});

		return result;
	}

	setHeaders(headers) {
		this.headers = headers;
	}

	setRequestOptions(requestOptions) {
		this.requestOptions = requestOptions;
	}

	setSuccessHandler(successHandler) {
		this.successHandler = successHandler;
	}

	setParser(parser) {
		this.parser = parser;
	}

	triggerSubmit() {
		this.shadowRoot.querySelector('form').dispatchEvent(new Event('submit'));
	}

	setErrors(errors) {
		const formErrors = errors.__all__;

		this.removeErrors(); // First we'll just clean any previous errors

		if (!!formErrors) {
			this.errors.classList.add('show');
			formErrors.forEach((error, index) => {
				const item = this.newElement('li');

				item.textContent = error.message;
				this.errors.appendChild(item);
			});
		}

		Object.entries(errors).forEach((entry, index) => {
			const selector = this.fieldTranslations && this.fieldTranslations[entry[0]] || entry[0],
				field = this.querySelector(`#${selector}`);
			if (!!field) {
				field.setErrors(entry[1]);
			}
		});
	}

	removeErrors() {
		this.errors.innerHTML = '';
		this.errors.classList.remove('show');
		this.querySelectorAll('sablono-field').forEach(field => {
			field.removeErrors();
		});
	}

	populateForm(blob) {
		Object.entries(blob).forEach((entry, index) => {
			const selector = this.fieldTranslations && this.fieldTranslations[entry[0]] || entry[0],
				field = this.querySelector(`#${selector}`);
			if (!!field) {
				field.setValue(entry[1]);
			}
		});
	}

	setFieldTranslations(fieldTranslations) {
		this.fieldTranslations = fieldTranslations;
	}
}
