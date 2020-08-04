import { BoxComponent } from '../../components/box.js';
import { FieldComponent } from '../../components/field.js';
import { FormComponent } from '../../components/form.js';
import { GridComponent } from '../../components/grid.js';
import { Component } from '../../fiu/component.js';

export class IndexPageComponent extends Component {
	static tagName = 'index-page';
	static template = 'components/index-page';
	static stylesheets = [
		'meta',
		'palette',
		'main',
		'font-awesome',
		'normalize',
		'components/index-page',
	];
	static registerComponents = [
		BoxComponent,
		GridComponent,
		FormComponent,
		FieldComponent,
	];

	constructor() {
		super(IndexPageComponent);
		console.log('IndexPageComponent constructor finished');
	}
}
