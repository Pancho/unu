// include:media/js/sablono.js
// include:media/js/unu/unu.js
'use strict';

Djangoutils.Unu.Index = (function () {
	var r = {
		initAnalyze: function () {
			Mavor.delegateEvent('.unu-analyze', 'click', function (ev) {
				var container = ev.target.closest('.content');

				ev.preventDefault();

				// Remove existing definition lists
				container.querySelectorAll('dl').forEach(function (elm) {
					container.removeChild(elm);
				});

				Mavor.get(ev.target.getAttribute('href')).then(function (response) {
					return response.json();
				}).then(function (data) {
					var definitionList = Mavor.createElement('<dl class="inline-block-children"></dl>');

					if (data['status'] === 'ok') {
						data['recommendations'].forEach(function (blob, index) {
							definitionList.appendChild(Mavor.createElement('<dt>' + blob['app'] + '</dt>'));
							definitionList.appendChild(Mavor.createElement('<dd>' + blob['text'] + '</dd>'));
						});

						Mavor.insertBefore(ev.target, Mavor.elementToString(definitionList));
					}
				});
			});
		},
		initAddClosureCompiler: function () {
			Mavor.delegateEvent('.unu-closure-compiler', 'click', function (ev) {
				ev.preventDefault();

				Mavor.post(ev.target.getAttribute('href')).then(function (response) {
					return response.json();
				}).then(function (data) {
				});
			});
		},
		initFixers: function () {
			Mavor.delegateEvent('.fixer', 'click', function (ev) {
				ev.preventDefault();

				Mavor.post(ev.target.getAttribute('href')).then(function (response) {
					return response.json();
				}).then(function (data) {
					var content = ev.target.closest('.content'),
						log = ev.target.closest('section').querySelector('.log'),
						logList = Mavor.createElement('<ol></ol>');

					if (!!log) {
						ev.target.closest('section').removeChild(log);
					}

					log = Mavor.createElement('<div class="log content"></div>');
					if (data['status'] === 'ok') {
						data['result'].forEach(function (line, index) {
							logList.appendChild(Mavor.createElement('<li class="border-grey-10">' + line + '</li>'));
						});

						log.appendChild(logList);
						Mavor.insertBefore(content, Mavor.elementToString(log));
					}
				});
			});
		}
	}, u = {
		initialize: function () {
			Sablono.initialize();
			r.initAnalyze();
			r.initAddClosureCompiler();
			r.initFixers();
		},
	};

	return u;
})();

Djangoutils.Unu.Index.initialize();
