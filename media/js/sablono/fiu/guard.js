export class Guard {
	constructor() {}

	/**
	 * This is the method that needs overriding.
	 */
	async run(router, route) {
		return true;
	}

	/**
	 * If you override this method, you're probably in quite some trouble... leave it.
	 */
	async guard(router, route) {
		return await this.run(router, route);
	}
}
