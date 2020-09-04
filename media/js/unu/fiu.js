// include:media/js/sablono.js
// include:media/js/unu/unu.js
'use strict';

Djangoutils.Unu.Fiu = (function () {
	var r = {
		initFiuFiles: function () {
			Mavor.delegateEvent('.unu-fiu-get-files', 'click', function (ev) {
				var container = ev.target.closest('.content');

				ev.preventDefault();

				// Remove existing definition lists
				container.querySelectorAll('p').forEach(function (elm) {
					container.removeChild(elm);
				});

				Mavor.get(ev.target.getAttribute('href')).then(function (response) {
					return response.json();
				}).then(function (data) {
					var paragraph = Mavor.createElement('<p>Fiu files have been successfully fetched from the repository.</p>');

					if (data['status'] === 'ok') {
						Mavor.insertBefore(ev.target, Mavor.elementToString(paragraph));
					}
				});
			});
		},
		initPostFormAndPrintLog: function (formSelector, logId) {
			Mavor.delegateEvent(formSelector, 'submit', function (ev) {
				ev.preventDefault();

				Mavor.post(ev.target.getAttribute('action'), {
					body: new FormData(ev.target),
				}).then(function (response) {
					return response.json();
				}).then(function (data) {
					/* CSS: #app-log li */
					/* CSS: #component-log li */
					/* CSS: #page-log li */
					var log = document.getElementById(logId);

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
		}
	}, u = {
		initialize: function () {
			Sablono.initialize();
			r.initFiuFiles();
			r.initPostFormAndPrintLog('#new-fiu-app', 'app-log');
			r.initPostFormAndPrintLog('#new-fiu-component', 'component-log');
			r.initPostFormAndPrintLog('#new-fiu-page', 'page-log');
		},
	};

	return u;
})();

Djangoutils.Unu.Fiu.initialize();
