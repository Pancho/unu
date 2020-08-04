import { Guard } from './fiu/guard.js';

export class SablonoGuard extends Guard {
	constructor() {
		super();
	}

	async run(router, route) {
		const token = window.localStorage.getItem('auth-token');

		if (!!token) {
			try {
				// One has to use native api here, since the App (and there fore http instance) is not ready yet if you're hitting this immediately
				const response = await window.fetch(`/sablono/api/token-valid?token=${token}`, {
						method: 'GET',
						headers: {
							'Accept': 'application/json, text/plain, */*',
							'X-Requested-With': 'XMLHttpRequest',
						}
					}),
					json = await response.json();

				if (json.status === 'ok' && json.valid) {
					document.querySelector('sablono-header').setAttribute('authenticated', 'authenticated');
					return true;
				} else {
					await router.navigate(`${router.authenticationUrl}#${route.path}`);
					document.querySelector('sablono-header').setAttribute('authenticated', '');
					return false;
				}
			} catch (e) {
				await router.navigate(`${router.authenticationUrl}#${route.path}`);
				document.querySelector('sablono-header').setAttribute('authenticated', '');
				return false;
			}

		} else {
			await router.navigate(`${router.authenticationUrl}#${route.path}`);
			document.querySelector('sablono-header').setAttribute('authenticated', '');
			return false;
		}

	}
}
