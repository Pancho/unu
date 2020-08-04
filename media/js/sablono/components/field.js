import { Component } from '../fiu/component.js';

/*
* TODO: We still need file upload field, radio group, checkboxes(?); others (simple ones) can be covered by this one
* */
export class FieldComponent extends Component {
	static tagName = 'sablono-field';
	static template = 'components/field';
	static stylesheets = [
		'palette',
		'font-awesome',
		'normalize',
		'components/field',
	];

	label;
	help;
	errors;

	constructor() {
		super(FieldComponent);
		console.log('FieldComponent constructor finished');
	}

	onTemplateLoaded() {
		const control = this.querySelector(':scope > *'),
			form = this.closest('sablono-form');

		if (!control) {
			throw new Error('You need to provide the actual HTML control (input, select...) that will provide the user input interface. This is just a wrapper. Be aware, that you can and may just forgo these custom elements and just use plain ol\' forms without any special handling.');
		}

		if (!form) {
			throw new Error('You cannot place a sablono-field into an element that\'s not a sablono-form. Future is awesome, but there is always a price to be paid.');
		}

		control.addEventListener('keyup', function (e) {
			if (e.keyCode === 13) {
				form.triggerSubmit();
			}
		});
		this.label.textContent = this.attribute('label');
		this.label.addEventListener('click', event => {
			control.focus();
		});
		this.label.setAttribute('for', this.attribute('label-for'));
	}

	populateFields() {
		return {
			errors: '.errors',
			label: 'label',
			help: '.help',
		};
	}

	validate() {
		const elm = this.querySelector(':scope > *');
		elm.reportValidity();
		return elm.checkValidity();
	}

	compileValues(fieldTranslations) {
		const elm = this.querySelector(':scope > *'),
			fieldName = fieldTranslations && fieldTranslations[elm.getAttribute('name')] || elm.getAttribute('name');

		return {
			[fieldName]: elm.value,
		};
	}

	setErrors(errors) {
		if (!!errors) {
			this.errors.classList.add('show');
			errors.forEach((error, index) => {
				const item = this.newElement('li');

				item.textContent = error.message;
				this.errors.appendChild(item);
			});
		}
	}

	removeErrors() {
		this.errors.innerHTML = '';
		this.errors.classList.remove('show');
	}

	setValue(value) {
		const elm = this.querySelector(':scope > *'),
			selectValue = elm.querySelector(`[value="${value}"]`),
			tagName = elm.tagName.toLowerCase(),
			elmType = elm.getAttribute('type');

		if (tagName === 'select' && !!selectValue) {
			selectValue.selected = true;
		} else if (elmType === 'checkbox' || elmType === 'radio') {
			elm.checked = !!value;
		} else {
			// This works for everything but selects and radio/checkbox inputs... who would have known... Ref: jQuery
			elm.value = value;
		}


	}
}
