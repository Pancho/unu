import { Component } from '../../fiu/component.js';

export class SiteHealthPageComponent extends Component {
	static tagName = 'site-health-page';
	static template = 'components/site-health-page';
	static stylesheets = [
		'meta',
		'palette',
		'font-awesome',
		'normalize',
		'components/site-health-page',
	];

	constructor() {
		super(SiteHealthPageComponent);
		console.log('SiteHealthPageComponent constructor finished');
	}
}
