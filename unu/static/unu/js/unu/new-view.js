// include:media/js/sablono.js
// include:media/js/unu/unu.js
'use strict';

Djangoutils.Unu.NewView = (function () {
	var r = {
		initPopulateApps: function () {
			document.querySelectorAll('.populate-with-apps').forEach(function (elm, index) {
				var url = elm.dataset['getAppsUrl'];

				if (elm.dataset['modelsOnly']) {
					url += '?' + Mavor.params({
						withModels: true,
					});
				}

				fetch(url).then(function (response) {
					return response.json();
				}).then(function (data) {
					if (data['status'] === 'ok') {
						// Empty the existing options
						while (elm.lastElementChild) {
							// But remove from the end, much easier for computer to trim the list from that end.
							elm.removeChild(elm.lastElementChild);
						}
						data['apps'].forEach(function (app, index) {
							elm.appendChild(Mavor.createElement('<option value="' + app + '">' + app + '</option>'));
						});
					}
				});
			});
		},
		refreshModels: function (elm) {
			var ref = document.querySelector(elm.dataset['ref']),
				url = elm.dataset['getModelsUrl'] + '?' + Mavor.params({
					app: ref.value,
				});

			if (ref.querySelectorAll('option').length === 0) {
				setTimeout(function () {
					r.refreshModels(elm);
				}, 1000);
				return;
			}

			fetch(url).then(function (response) {
				return response.json();
			}).then(function (data) {
				if (data['status'] === 'ok') {
					// Empty the existing options
					while (elm.lastElementChild) {
						// But remove from the end, much easier for computer to trim the list from that end.
						elm.removeChild(elm.lastElementChild);
					}
					data['models'].forEach(function (model, index) {
						elm.appendChild(Mavor.createElement('<option value="' + model + '">' + model + '</option>'));
					});
				}
			});
		},
		initPopulateModels: function () {
			document.querySelectorAll('.populate-with-models').forEach(function (elm, index) {
				r.refreshModels(elm);
			});

			Mavor.delegateEvent('.populate-with-apps', 'change', function (ev) {
				document.querySelectorAll('.populate-with-models').forEach(function (elm, index) {
					r.refreshModels(elm);
				});
			});
		},
		camelPad: function (str) {
			return str
				// Look for long acronyms and filter out the last letter
				.replace(/([A-Z]+)([A-Z][a-z])/g, ' $1 $2')
				// Look for lower-case letters followed by upper-case letters
				.replace(/([a-z\d])([A-Z])/g, '$1 $2')
				// Look for lower-case letters followed by numbers
				.replace(/([a-zA-Z])(\d)/g, '$1 $2')
				.replace(/^./, function (str) {
					return str.toUpperCase();
				})
				// Remove any white space left around the word
				.trim();
		},
		initLiveSlugify: function () {
			Mavor.delegateEvent('.live-slugify', 'input', function (ev) {
				var parent = ev.target.closest('li');

				parent.querySelectorAll('.live-slug').forEach(function (elm, index) {
					parent.removeChild(elm);
				});

				parent.append(Mavor.createElement('<p class="live-slug">' + Mavor.slugify(r.camelPad(ev.target.value)) + '</p>'));
			});
		},
		initForm: function () {
			Mavor.delegateEvent('form', 'submit', function (ev) {
				ev.preventDefault();

				Mavor.post(ev.target.getAttribute('action'), {
					body: new FormData(ev.target),
				}).then(function (response) {
					return response.json();
				}).then(function (data) {
					/* CSS: #log li */
					var log = document.getElementById('log');

					while (log.lastElementChild) {
						log.removeChild(log.lastElementChild);
					}

					if (data['status'] === 'ok') {
						data['log'].forEach(function (entry, index) {
							log.appendChild(Mavor.createElement('<li class="border-grey-10">[' + index + ']: ' + entry + '</li>'));
						});
					}
				});
			});
		},
		initPopulateUrlNames: function () {
			document.querySelectorAll('.populate-urls').forEach(function (elm, index) {
				fetch(elm.dataset['getUrls']).then(function (response) {
					return response.json();
				}).then(function (data) {
					if (data['status'] === 'ok') {
						// Empty the existing options
						while (elm.lastElementChild) {
							// But remove from the end, much easier for computer to trim the list from that end.
							elm.removeChild(elm.lastElementChild);
						}
						data['urlNames'].forEach(function (urlName, index) {
							elm.appendChild(Mavor.createElement('<option value="' + urlName + '">' + urlName + '</option>'));
						});
					}
				});
			});
		},
	}, u = {
		initialize: function () {
			Sablono.initialize();
			r.initPopulateApps();
			r.initPopulateModels();
			r.initPopulateUrlNames();
			r.initLiveSlugify();
			r.initForm();
		},
	};

	return u;
})();

Djangoutils.Unu.NewView.initialize();
