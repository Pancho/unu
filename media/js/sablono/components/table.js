import { Component } from '../fiu/component.js';

export class TableComponent extends Component {
	static tagName = 'sablono-table';
	static template = 'components/table';
	static stylesheets = [
		'palette',
		'font-awesome',
		'normalize',
		'components/table',
	];

	thead;
	tbody;
	tfoot;

	constructor() {
		super(TableComponent);
		console.log('TableComponent constructor finished');
	}

	onTemplateLoaded() {
		const header = this.attribute('header');

		if (!!header) {
			this.thead.classList.add('show');
			header.split(',').forEach((headerText, index) => {
				const heading = this.newElement('th');
				heading.textContent = headerText.trim();
				this.thead.querySelector('tr').append(heading);
			});
		}
	}

	populateFields() {
		return {
			thead: 'thead',
			tbody: 'tbody',
			tfoot: 'tfoot',
		};
	}

	updateBody(data) {
		this.tbody.innerHTML = '';
		data.forEach((dataRow, index) => {
			const row = this.newElement('tr');

			dataRow.forEach((dataCell, index) => {
				const cell = this.newElement('td');

				if (Array.isArray(dataCell)) {
					dataCell.forEach((part, index) => {
						cell.append(part);
					});
				} else {
					cell.append(dataCell);
				}
				row.append(cell);
			});

			this.tbody.append(row);
		});
	}
}
