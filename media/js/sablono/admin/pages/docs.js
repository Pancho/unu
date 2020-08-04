import { BoxComponent } from '../../components/box.js';
import { ChartComponent } from '../../components/chart.js';
import { GridComponent } from '../../components/grid.js';
import { Component } from '../../fiu/component.js';

export class DocsPageComponent extends Component {
	static tagName = 'docs-page';
	static template = 'components/docs-page';
	static stylesheets = [
		'meta',
		'palette',
		'font-awesome',
		'normalize',
		'main',
		'components/docs-page',
	];
	static registerComponents = [
		BoxComponent,
		GridComponent,
		ChartComponent,
	];

	grids;

	constructor() {
		super(DocsPageComponent);
		console.log('DocsPageComponent constructor finished');
	}

	onTemplateLoaded() {
	}

	populateFields() {
		return {
			grids: '|all|sablono-grid'
		}
	}
}
