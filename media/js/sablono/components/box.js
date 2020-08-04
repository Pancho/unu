import { Component } from '../fiu/component.js';

export class BoxComponent extends Component {
	static tagName = 'sablono-box';
	static template = 'components/box';
	static stylesheets = [
		'palette',
		'font-awesome',
		'normalize',
		'components/box',
	];

	title;
	close;
	collapseRestore;
	box;
	section;

	constructor() {
		super(BoxComponent);
		console.log('BoxComponent constructor finished');
	}

	onTemplateLoaded() {
		const subtitle = this.attribute('subtitle'),
			hideCollapse = this.attribute('hide-collapse'),
			sectionHeight = this.attribute('section-height');

		this.title.textContent = this.attribute('title');

		if (!!subtitle) {
			const span = this.newElement('span');
			span.textContent = this.attribute('subtitle');
			this.title.append(span);
		}

		if (this.attribute('show-close') === 'true') {
			this.close.classList.add('show');
			this.close.addEventListener('click', (event) => {
				this.remove();
			});
		}

		if (hideCollapse === 'true') {
			this.collapseRestore.classList.add('hide');
		}

		this.collapseRestore.addEventListener('click', (event) => {
			if (this.collapseRestore.dataset.collapsed === 'true') {
				this.collapseRestore.classList.remove('fa-window-restore');
				this.collapseRestore.classList.add('fa-minus-square');
				this.collapseRestore.dataset.collapsed = null;
				this.box.classList.remove('collapsed');

			} else {
				this.collapseRestore.classList.remove('fa-minus-square');
				this.collapseRestore.classList.add('fa-window-restore');
				this.collapseRestore.dataset.collapsed = 'true';
				this.box.classList.add('collapsed');
			}
		});

		if (!!sectionHeight) {
			const stylesheet = new CSSStyleSheet();
			stylesheet.replaceSync(`.box section {max-height:${sectionHeight}px;`);
			this.shadowRoot.adoptedStyleSheets = [...this.shadowRoot.adoptedStyleSheets, stylesheet];
		}
	}

	populateFields() {
		return {
			title: 'header h3',
			close: 'header .close',
			collapseRestore: 'header .collapse',
			box: '.box',
			section: 'section',
		}
	}
}
