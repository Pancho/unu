// include:media/js/mavor.js
'use strict';
var Sablono = (function () {
	var r = {
		initTabbedBoxes: function () {
			Mavor.delegateEvent('.box-tabbed .tabs li', 'click', function (ev) {
				var tab = this;

				ev.preventDefault();

				tab.closest('.box').querySelectorAll('.tabs li').forEach(function (li) {
					li.classList.remove('selected', 'border-blue-50', 'bg-white');
				});
				tab.closest('.box').querySelectorAll('.tabs-content li').forEach(function (li) {
					li.style.display = 'none';
				});

				tab.classList.add('selected', 'border-blue-50', 'bg-white');
				document.querySelector('#' + tab.dataset.target).style.display = 'block';
			}, 'tabbed-boxes');
		},
		initNotifications: function () {
			Mavor.delegateEvent('#notifications .close', 'click', function (ev) {
				var item = this;

				ev.preventDefault();

				item.closest('li').style.display = 'none';
				item.closest('li').parentNode.removeChild(item);
			}, 'notifications');
		},
		setElementGrid: function (elm, rows, columns) {
			elm.style['grid-template-rows'] = 'repeat(' + rows + ', 1fr)';
			elm.style['grid-template-columns'] = 'repeat(' + columns + ', 1fr)';
		},
		initGridData: function () {
			document.querySelectorAll('[data-grid]').forEach(function (elm, i) {
				var grid = elm.dataset['grid'],
					gridParts = [],
					rows = '',
					columns = '';

				if (!!grid) {
					gridParts = grid.split('/');

					rows = gridParts[0];
					columns = gridParts[1];

					r.setElementGrid(elm, rows, columns);
				}
			});

			document.querySelectorAll('[data-rows]').forEach(function (elm, i) {
				elm.style['grid-row'] = elm.dataset['rows'];
			});

			document.querySelectorAll('[data-columns]').forEach(function (elm, i) {
				elm.style['grid-column'] = elm.dataset['columns'];
			});
		}
	}, u = {
		initialize: function () {
			r.initGridData();
			r.initTabbedBoxes();
			r.initNotifications();
		}
	};

	return u;
})();
