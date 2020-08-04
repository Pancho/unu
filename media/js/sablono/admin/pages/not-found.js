import { Component } from '../../fiu/component.js';

export class NotFoundComponent extends Component {
	static tagName = 'not-found-page';
	static template = 'components/not-found-page';
	static stylesheets = [
		'meta',
		'palette',
		'font-awesome',
		'normalize',
		'components/not-found-page',
	];

	constructor() {
		super(NotFoundComponent);
		console.log('NotFoundComponent constructor finished');
	}
}
