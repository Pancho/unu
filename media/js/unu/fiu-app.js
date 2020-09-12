// include:media/js/sablono.js
// include:media/js/unu/unu.js
'use strict';

Djangoutils.Unu.FiuApp = (function () {
	var r = {
		initPostFormAndPrintLog: function (formSelector, logId) {
			Mavor.delegateEvent(formSelector, 'submit', function (ev) {
				ev.preventDefault();

				Mavor.post(ev.target.getAttribute('action'), {
					body: new FormData(ev.target),
				}).then(function (response) {
					return response.json();
				}).then(function (data) {
					/* CSS: .app-data */
					/* CSS: .log li */
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
			r.initPostFormAndPrintLog('#new-fiu-component', 'component-log');
			r.initPostFormAndPrintLog('#new-fiu-page', 'page-log');

		}
	};

	return u;
})();

Djangoutils.Unu.FiuApp.initialize();
