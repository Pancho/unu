import { Component } from '../fiu/component.js';

export class HeaderComponent extends Component {
	static tagName = 'sablono-header';
	static template = 'components/header';
	static stylesheets = [
		'meta',
		'palette',
		'font-awesome',
		'normalize',
		'components/header',
	];

	logout;
	login;

	constructor() {
		super(HeaderComponent);
		console.log('HeaderComponent constructor finished');
	}

	onTemplateLoaded() {
		this.logout.addEventListener('click', event => {
			event.preventDefault();
			window.localStorage.removeItem('auth-token');
			this.app.router.navigate('');
			this.setAttribute('authenticated', '');
		});
		this.login.addEventListener('click', event => {
			event.preventDefault();
			this.app.router.navigate('/login');
		});
		this.setAuthenticated(!!window.localStorage.getItem('auth-token'));
	}

	populateFields() {
		return {
			logout: '#logout',
			login: '#login',
		}
	}

	observeAuthenticated(oldValue, newValue) {
		if (newValue === 'authenticated') {
			this.setAuthenticated(true);
		} else {
			this.setAuthenticated(false);
		}
	}

	setAuthenticated(authenticated) {
		if (!this.login || !this.logout) {
			return;
		}

		if (authenticated) {
			this.logout.closest('li').classList.remove('hide');
			this.login.closest('li').classList.add('hide');
		} else {
			this.logout.closest('li').classList.add('hide');
			this.login.closest('li').classList.remove('hide');
		}
	}
}
