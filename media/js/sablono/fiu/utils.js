export class Utils {
	static cssCache = {};
	static cssQueue = [];
	static templateCache = {};
	static templateQueue = {};
	static domParser = new DOMParser();

	static applyCss(stylesheets, shadowRoot) {
		stylesheets.forEach((name, index) => {
			if (!!Utils.cssCache[name]) {
				shadowRoot.adoptedStyleSheets = [...shadowRoot.adoptedStyleSheets, Utils.cssCache[name]];
			} else if (!!Utils.cssQueue[name]) {
				Utils.cssQueue[name].push(shadowRoot);
			} else {
				if (!Utils.cssQueue[name]) {
					Utils.cssQueue[name] = [];
				}
				Utils.cssQueue[name].push(shadowRoot);

				fetch('/media/css/sablono/' + name.toLowerCase() + '.css', {
					method: 'GET',
				}).then((response) => {
					return response.text();
				}).then((css) => {
					const styleSheet = new CSSStyleSheet();
					styleSheet.replaceSync(css);
					Utils.cssCache[name] = styleSheet;
					Utils.cssQueue[name].forEach((root, index) => {
						root.adoptedStyleSheets = [...root.adoptedStyleSheets, styleSheet];
					});
				});
			}
		});
	}

	static getTemplateHTML(name, shadowRoot, resolve) {
		resolve = resolve || function () {};
		if (!!Utils.templateCache[name]) {
			shadowRoot.append(Utils.templateCache[name].querySelector('template').content.cloneNode(true));
			resolve();
		} else if (!!Utils.templateQueue[name]) {
			Utils.templateQueue[name].push({
				shadowRoot: shadowRoot,
				resolve: resolve,
			});
		} else {
			if (!Utils.templateQueue[name]) {
				Utils.templateQueue[name] = [];
			}
			Utils.templateQueue[name].push({
				shadowRoot: shadowRoot,
				resolve: resolve,
			});

			fetch('/media/templates/sablono/' + name.toLowerCase() + '.html', {
				method: 'GET',
			}).then(response => response.text()).then((html) => {
				const doc = Utils.domParser.parseFromString(html, 'text/html');
				Utils.templateCache[name] = doc;
				let blob = Utils.templateQueue[name].pop();
				while (blob) {
					blob.shadowRoot.append(doc.querySelector('template').content.cloneNode(true));
					blob.resolve();
					blob = Utils.templateQueue[name].pop();
				}
			});
		}
	}
}
