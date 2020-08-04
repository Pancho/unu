import Highcharts from 'https://code.highcharts.com/es-modules/masters/highcharts.src.js';
import { Component } from '../fiu/component.js';

export class ChartComponent extends Component {
	static tagName = 'sablono-chart';
	static template = 'components/chart';
	static stylesheets = [
		'palette',
		'font-awesome',
		'normalize',
		'components/chart',
	];

	container;

	constructor() {
		super(ChartComponent);
		console.log('ChartComponent constructor finished');
	}

	onTemplateLoaded() {
		Highcharts.chart(this.container, {
			chart: {
				type: 'bar',
			},
			title: {
				text: 'Fruit Consumption',
			},
			xAxis: {
				categories: ['Apples', 'Bananas', 'Oranges'],
			},
			yAxis: {
				title: {
					text: 'Fruit eaten',
				},
			},
			series: [{
				name: 'Jane',
				data: [1, 0, 4],
			}, {
				name: 'John',
				data: [5, 7, 3],
			}],
		});
	}

	observeData(oldValue, newValue) {

	}

	populateFields() {
		return {
			container: '#container',
		}
	}
}
