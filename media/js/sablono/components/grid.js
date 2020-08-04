import { Component } from '../fiu/component.js';

export class GridComponent extends Component {
	static tagName = 'sablono-grid';
	static template = 'components/grid';
	static stylesheets = [
		'normalize',
		'components/grid',
	];

	constructor() {
		super(GridComponent);
		console.log('GridComponent constructor finished');
	}

	onTemplateLoaded() {
		const rows = this.attribute('rows') || '1',
			columns = this.attribute('columns') || '1';
		this.shadowRoot.querySelector('slot').style.gridTemplateRows = 'repeat(' + rows + ', 1fr)';
		this.shadowRoot.querySelector('slot').style.gridTemplateColumns = 'repeat(' + columns + ', 1fr)';
		this.querySelectorAll(':scope > *').forEach((elm, index) => {
			const rowSpan = elm.getAttribute('row-span'),
				columnSpan = elm.getAttribute('column-span');

			if (!!rowSpan) {
				elm.style.gridRow = rowSpan;
			}
			if (!!columnSpan) {
				elm.style.gridColumn = columnSpan;
			}
		});
	}
}
