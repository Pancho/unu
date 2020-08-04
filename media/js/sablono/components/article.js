import { Component } from '../fiu/component.js';

export class ArticleComponent extends Component {
	static tagName = 'sablono-article';
	static template = 'components/article';
	static stylesheets = [
		'palette',
		'font-awesome',
		'normalize',
		'components/article',
	];

	h1;
	div;

	constructor() {
		super(ArticleComponent);
		console.log('ArticleComponent constructor finished');
	}

	onTemplateLoaded() {

	}

	populateFields() {
		return {
			h1: 'h1',
			div: 'div',
		}
	}
}
