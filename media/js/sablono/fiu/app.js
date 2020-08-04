import { Authentication } from './authentication.js';
import { Component } from './component.js';
import { Http } from './http.js';
import { Router } from './router.js';
import { Utils } from './utils.js';

export class App {
	static instance;
	static appReady;
	router = null;
	http = null;

	constructor(
		routeRoot,
		homePage,
		notFound,
		routes,
		defaultPageName,
		defaultComponents,
		defaultStylesheets,
		authenticationClass,
		authenticationUrl,
		httpEndpointStub,
		onAppReady,
	) {
		let authentication;

		if (!!App.instance) {
			throw new Error('Only one instance of App allowed');
		}

		if (!!defaultStylesheets) {
			Utils.applyCss(defaultStylesheets, document);
		}

		App.instance = this;
		App.appReady = new Promise(resolve => {
			// We must delay the initialization of the root components and router, so that the Component classes have time to subscribe to
			// router's link handling, even if just by pushing everything to the end of the stack
			setTimeout(() => {
				if (!!defaultComponents) {
					defaultComponents.forEach((component) => {
						Component.attachObservedAttributes(component);
						customElements.define(component.tagName, component);
					});
				}

				this.router = new Router(routeRoot, homePage, notFound, routes, defaultPageName, authenticationUrl);

				if (!!authenticationClass) {
					authentication = new authenticationClass();
				} else {
					authentication = new Authentication();
				}

				this.http = new Http(httpEndpointStub, authentication);

				onAppReady.forEach(fn => fn());

				resolve();
			});
		});

		return this;
	}
}
