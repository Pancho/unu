import { AdminPageComponent } from './sablono/admin/pages/admin.js';
import { DocsPageComponent } from './sablono/admin/pages/docs.js';
import { IndexPageComponent } from './sablono/admin/pages/index.js';
import { LoginPageComponent } from './sablono/admin/pages/login.js';
import { NotFoundComponent } from './sablono/admin/pages/not-found.js';
import { SiteHealthPageComponent } from './sablono/admin/pages/site-health.js';
import { HeaderComponent } from './sablono/components/header.js';
import { NavigationComponent } from './sablono/components/navigation.js';
import { App } from './sablono/fiu/app.js';
import { SablonoAuthentication } from './sablono/sablono-authentication.js';
import { SablonoGuard } from './sablono/sablono-guard.js';

class Sablono extends App {
	static routeRoot = 'https://localhost/sablono/demo';
	static homePage = {
		component: IndexPageComponent,
	};
	static notFound = {
		component: NotFoundComponent,
	};
	static routes = [
		{
			path: '/admin',
			component: AdminPageComponent,
			guard: SablonoGuard,
		},
		{
			path: '/docs',
			component: DocsPageComponent,
		},
		{
			path: '/site-health',
			component: SiteHealthPageComponent,
			guard: SablonoGuard,
		},
		{
			path: '/login',
			component: LoginPageComponent,
		},
	];
	static defaultPageName = 'Sablono Demo';
	// All of your first level components, the ones that need to be loaded before the page renders (always present or listed in the
	// routes - pages)
	static defaultComponents = [
		HeaderComponent,
		NavigationComponent,
		AdminPageComponent,
		IndexPageComponent,
		NotFoundComponent,
		DocsPageComponent,
		LoginPageComponent,
		SiteHealthPageComponent,
	];
	static defaultStylesheets = [
		'meta',
		'normalize',
		'font-awesome',
		'fonts',
	];
	static authenticationClass = SablonoAuthentication;
	static authenticationUrl = '/login';
	static httpEndpointStub = 'https://localhost/sablono/api/';
	static onAppReady = [
		() => {
			// We'll just engage the token refresh here
			// So since jwt tokens can only be revoked, with effect, on the front end, renewing and using the "old" one is benign in our case
			setTimeout(() => {
				setInterval(() => {
					App.instance.http.post('/token-refresh')
						.then(response => response.json())
						.then(data => {
							if (data.status === 'ok') {
								window.localStorage.setItem('auth-token', data.token);
							} // If not, just ignore, since it's of no consequence and we'll just be trying to refresh an invalid token
						});
				}, 60 * 60 * 1000); // And then do it every hour.
			}, 10 * 60 * 1000); // Try after 10 minutes for the first time, not sooner, it would make little sense to do so
		},
	];

	constructor() {
		super(
			Sablono.routeRoot,
			Sablono.homePage,
			Sablono.notFound,
			Sablono.routes,
			Sablono.defaultPageName,
			Sablono.defaultComponents,
			Sablono.defaultStylesheets,
			Sablono.authenticationClass,
			Sablono.authenticationUrl,
			Sablono.httpEndpointStub,
			Sablono.onAppReady,
		);
	}
}

new Sablono();


/*
* Welcome
* WebCompoents
** Change in arhitecture
** Framewroks
** Vanilla
** Sablono Rationale
*** simplicity
*** JS is still the best and worst
*** speed, performace, baggage (npm, https://github.com/olivernn/lunr.js/issues/401#issuecomment-494917496)
** End of web as we know it? Hell no!

* Framewrok
* Classes
** App
** Authentication
** Component
** Http
** Mavor
** Router
** Utils
* Weird stuff
** links
** observedAttributes
** templates
** CSS
**

* Sablono
** Article
** Box
** Chart
** Grid
** Header
** Navigation

* */
