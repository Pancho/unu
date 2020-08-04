import { Component } from '../fiu/component.js';

export class NavigationComponent extends Component {
	static tagName = 'sablono-navigation';
	static template = 'components/navigation';
	static stylesheets = [
		'meta',
		'palette',
		'font-awesome',
		'normalize',
		'components/navigation',
	];

	nav;

	constructor() {
		super(NavigationComponent);
		console.log('NavigationComponent constructor finished');
	}

	onTemplateLoaded() {
		// If I had selected any other element accessible from document, I might have trouble as it might resize that element along with nav
		// And trigger this again... ad-infinitum, and possibly ignite the computer (after a couple of years of doing that, easily solvable
		// by a hammer or an F5)
		const routerOutlet = document.querySelector('router-outlet'),
			resizeObserver = new ResizeObserver(entries => {
				entries.forEach((elm, index) => {
					this.nav.style.height = `${elm.target.offsetHeight}px`;
				});
			});
		resizeObserver.observe(routerOutlet);
	}

	populateFields() {
		return {
			nav: 'nav',
		}
	}
}
