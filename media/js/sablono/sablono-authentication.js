import { Authentication } from './fiu/authentication.js';

export class SablonoAuthentication extends Authentication {
	constructor() {
		super();
	}

	/**
	 * This method MUST return options whether you modified it or not or a new dict, just make sure you populate it with right params.
	 * @param options
	 * @returns {*}
	 */
	addAuthentication(options) {
		const token = window.localStorage.getItem('auth-token');
		options.headers['Authentication'] = `JWTToken ${token}`;
		return options;
	}
}
