// include:media/js/mavor.js
'use strict';
var Common = (function () {
	var r = {
		initImages: function () {
			var observer = null;

			if (!('IntersectionObserver' in window)) {
				document.querySelectorAll('img:not(.preload)').forEach(function (elm, key, parent) {
					var src = elm.dataset.src;


					if (src.indexOf('-2x.') >= 0) {
						elm.setAttribute('srcset', src);
						elm.setAttribute('src', src.replace('-2x', ''));
					} else {
						elm.setAttribute('src', src);
					}
				});
			} else {
				observer = new IntersectionObserver(function (entries) {
					entries.forEach(function (entry) {
						var img = null,
							src = '';

						if (entry.intersectionRatio > 0) {
							observer.unobserve(entry.target);
							img = entry.target;
							src = img.dataset.src;

							if (!src) {
								return;
							}

							if (src.indexOf('-2x.') >= 0) {
								img.setAttribute('srcset', src);
								img.setAttribute('src', src.replace('-2x', ''));
							} else {
								img.setAttribute('src', src)
							}
						}
					});
				}, {
					rootMargin: '50px 0px',
					threshold: 0.01
				});

				document.querySelectorAll('img:not(.preload)').forEach(function (elm, key, parent) {
					observer.observe(elm);
				});
			}
		}
	}, u = {
		initialize: function () {
			r.initImages();
		}
	};

	return u;
})();
Common.initialize();
