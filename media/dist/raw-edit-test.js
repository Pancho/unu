'use strict';
var Mavor = (function () {
	var r = {
		events: {},
		inlineElements: ['a', 'span', 'bdo', 'em', 'strong', 'dfn', 'code', 'samp', 'kbd', 'var', 'cite', 'abbr', 'acronym', 'q', 'sub', 'sup', 'tt', 'i', 'b', 'big', 'small', 'u', 's', 'strike', 'font', 'ins', 'del', 'pre', 'address', 'dt', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
		initEventDelegation: function (event, forceCapture) {
			document.addEventListener(event, function (ev) {
				r.events[event].forEach(function (blob, i) {
					var target = ev.target;
					for (; target && target !== document; target = target.parentNode) {
						if (target.matches(blob.selector)) {
							try {
								blob.handler.call(target, ev);
							} catch (e) {
								console.log(e);
							}
							break;
						}
					}
				});
			}, !!forceCapture);
		},
		formatHTML: function (node, level, indentCharacter) {
			var indentBefore = new Array(level + 1).join(indentCharacter),
				indentAfter = new Array(level).join(indentCharacter),
				textNode = null,
				i = 0,
				j = node.children.length;
			for (; i < j; i += 1) {
				if (r.inlineElements.indexOf(node.children[i].tagName.toLowerCase()) === -1) {
					textNode = document.createTextNode('\n' + indentBefore);
					node.insertBefore(textNode, node.children[i]);
					r.formatHTML(node.children[i], level + 1, indentCharacter);
					if (node.lastElementChild === node.children[i]) {
						textNode = document.createTextNode('\n' + indentAfter);
						node.appendChild(textNode);
					}
				} else {
					textNode = document.createTextNode('\n' + indentBefore);
					node.insertBefore(textNode, node.children[i]);
					textNode = document.createTextNode('\n' + indentAfter);
					node.appendChild(textNode);
				}
			}
			return node.innerHTML.replace(/^\s*$(?:\r\n?|\n)/gm, '');
		},
		easingOptions: {
			'linear': function (t) {
				return t;
			},
			'easeInQuad': function (t) {
				return t * t;
			},
			'easeOutQuad': function (t) {
				return t * (2 - t);
			},
			'easeInOutQuad': function (t) {
				return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
			},
			'easeInCubic': function (t) {
				return t * t * t;
			},
			'easeOutCubic': function (t) {
				return (--t) * t * t + 1;
			},
			'easeInOutCubic': function (t) {
				return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
			},
			'easeInQuart': function (t) {
				return t * t * t * t;
			},
			'easeOutQuart': function (t) {
				return 1 - (--t) * t * t * t;
			},
			'easeInOutQuart': function (t) {
				return t < 0.5 ? 8 * t * t * t * t : 1 - 8 * (--t) * t * t * t;
			},
			'easeInQuint': function (t) {
				return t * t * t * t * t;
			},
			'easeOutQuint': function (t) {
				return 1 + (--t) * t * t * t * t;
			},
			'easeInOutQuint': function (t) {
				return t < 0.5 ? 16 * t * t * t * t * t : 1 + 16 * (--t) * t * t * t * t;
			},
		},
	}, u = {
		noop: function () {
		},
		delegateEvent: function (selector, event, handler, namespace, forceCapture) {
			if (!r.events[event]) {
				r.events[event] = [];
				r.initEventDelegation(event, forceCapture);
			}
			r.events[event].push({
				selector: selector,
				namespace: namespace || 'global',
				handler: handler,
			});
		},
		removeEvent: function (event, selector, namespace) {
			r.events[event].forEach(function (blob, i) {
				if (blob.selector === selector && blob.namespace === namespace) {
					r.events[event].splice(i, 1);
				}
			});
		},
		scrollTo: function (destination, duration, easing, callback) {
			var start = window.pageYOffset,
				startTime = 'now' in window.performance ? performance.now() : new Date().getTime(),
				documentHeight = Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight),
				windowHeight = window.innerHeight || document.documentElement.clientHeight || document.querySelector('body').clientHeight,
				targetElement = document.querySelector(destination),
				destinationOffset = targetElement.offsetTop,
				destinationOffsetToScroll = Math.round(documentHeight - destinationOffset < windowHeight ? documentHeight - windowHeight : destinationOffset),
				scroll = function () {
					var now = 'now' in window.performance ? performance.now() : new Date().getTime(),
						time = Math.min(1, ((now - startTime) / duration)),
						timeFunction = r.easingOptions[easing](time);
					window.scroll(0, Math.ceil((timeFunction * (destinationOffsetToScroll - start)) + start));
					if (Math.abs(window.pageYOffset - destinationOffsetToScroll) < 2) {
						callback();
						return;
					}
					destinationOffset = targetElement.offsetTop;
					destinationOffsetToScroll = Math.round(documentHeight - destinationOffset < windowHeight ? documentHeight - windowHeight : destinationOffset);
					requestAnimationFrame(scroll);
				};
			duration = duration || 200;
			easing = easing || 'linear';
			callback = callback || u.noop;
			if (!('requestAnimationFrame' in window)) {
				window.scroll(0, destinationOffsetToScroll);
				callback();
				return;
			}
			scroll();
		},
		params: function (dictionary) {
			var result = [];
			Object.keys(dictionary).forEach(function (key) {
				result.push(encodeURIComponent(key) + '=' + encodeURIComponent(dictionary[key]));
			});
			return result.join('&');
		},
		get: function (urlName, config) {
			var url = document.querySelector('body').dataset[urlName] || urlName;
			if (urlName.indexOf('/') === 0) {
				url = urlName;
			}
			config = config || {};
			config.method = 'GET';
			return fetch(url, config);
		},
		post: function (urlName, config) {
			var url = document.querySelector('body').dataset[urlName] || urlName;
			if (urlName.indexOf('/') === 0) {
				url = urlName;
			}
			config = config || {};
			config.method = 'POST';
			config.credentials = 'include';
			if (!config.headers) {
				config.headers = {};
			}
			if (!config.headers['Accept']) {
				config.headers['Accept'] = 'application/json';
			}
			if (!config.headers['X-Requested-With']) {
				config.headers['X-Requested-With'] = 'XMLHttpRequest';
			}
			return fetch(url, config);
		},
		indentHTML: function (html, indentCharacter) {
			var div = document.createElement('div');
			html = html.replace(/\n/g, '')
				.replace(/[\t ]+</g, '<')
				.replace(/>[\t ]+</g, '><')
				.replace(/>[\t ]+$/g, '>');
			div.innerHTML = html.trim();
			return r.formatHTML(div, 0, indentCharacter || '\t');
		},
		windowWidth: function () {
			var body = document.querySelector('body');
			return window.innerWidth || document.documentElement.clientWidth || body.clientWidth;
		},
		debounce: function (cb, wait, immediate) {
			var timeout = null;
			return function (ev) {
				var context = this,
					later = function () {
						timeout = null;
						if (!immediate) {
							cb.apply(context, [ev]);
						}
					},
					callNow = immediate && !timeout;
				clearTimeout(timeout);
				timeout = setTimeout(later, wait);
				if (callNow) {
					cb.apply(context, [ev]);
				}
			};
		},
		arrayToCSV: function (array, delimiter) {
			delimiter = delimiter || ',';
			return array.map(function (currentValue, index, originalArray) {
				return currentValue.map(function (innerCurrentValue, innerIndex, innerOriginalArray) {
					if (isNaN(innerCurrentValue)) {
						return '\\' + innerCurrentValue.replace(/"/g, '""') + '\\';
					} else {
						return innerCurrentValue;
					}
				}).join(delimiter);
			}).join('\n');
		},
		chunk: function (array, size) {
			return Array.from({
				length: Math.ceil(array.length / size),
			}, function (currentValue, index) {
				return array.slice(index * size, index * size + size);
			});
		},
		countBy: function (array, callback) {
			return array.map(typeof callback === 'function' ? callback : function (val) {
				return val[callback];
			}).reduce(function (acc, val) {
				acc[val] = (acc[val] || 0) + 1;
				return acc;
			}, {});
		},
		deepFlatten: function (array) {
			return [].concat.apply([], array.map(function (currentValue) {
				return (Array.isArray(currentValue) ? u.deepFlatten(currentValue) : currentValue);
			}));
		},
		groupBy: function (array, callback) {
			return array.map(typeof callback === 'function' ? callback : function (currentValuie) {
				return currentValuie[callback];
			}).reduce(function (acc, val, i) {
				acc[val] = (acc[val] || []).concat(array[i]);
				return acc;
			}, {});
		},
		JSONToCSV: function (array, columns, delimiter) {
			delimiter = delimiter || ',';
			return [
				columns.join(delimiter),
			].concat(array.map(function (currentValue) {
				return columns.reduce(function (acc, key) {
					return '' + acc + (!acc.length ? '' : delimiter) + '"' + (!currentValue[key] ? '' : currentValue[key]) + '"';
				}, '');
			})).join('\n');
		},
		randomChoice: function (array) {
			return array[Math.floor(Math.random() * array.length)];
		},
		shuffle: function (array) {
			var temp,
				result = array.slice(0),
				arrayLength = result.length,
				i = 0;
			while (arrayLength) {
				i = Math.floor(Math.random() * (arrayLength -= 1));
				temp = [result[i], result[arrayLength]];
				result[arrayLength] = temp[0];
				result[i] = temp[1];
			}
			return result;
		},
		union: function (a, b) {
			return Array.from(new Set(a.concat(b)));
		},
		createElement: function (string) {
			var wrapper = document.createElement('div');
			wrapper.innerHTML = string;
			return wrapper.firstElementChild;
		},
		elementToString: function (htmlElm) {
			var wrapper = document.createElement('div');
			wrapper.appendChild(htmlElm);
			return wrapper.innerHTML;
		},
		isMobile: function () {
			return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
		},
		elementContains: function (parent, child) {
			return parent !== child && parent.contains(child);
		},
		insertAfter: function (afterElement, htmlString) {
			return afterElement.insertAdjacentHTML('afterend', htmlString);
		},
		insertBefore: function (beforeElement, htmlString) {
			return beforeElement.insertAdjacentHTML('beforebegin', htmlString);
		},
		insertBeforeEnd: function (beforeElement, htmlString) {
			return beforeElement.insertAdjacentHTML('beforeend', htmlString);
		},
		observeMutations: function (element, callback, options) {
			var observer = new MutationObserver(function (mutations) {
				return mutations.forEach(function (m) {
					return callback(m);
				});
			});
			observer.observe(element, Object.assign({
				childList: true,
				attributes: true,
				attributeOldValue: true,
				characterData: true,
				characterDataOldValue: true,
				subtree: true,
			}, options));
			return observer;
		},
		runAsync: function (fn) {
			var worker = new Worker(URL.createObjectURL(new Blob(['postMessage((' + fn + ')());'])));
			return new Promise(function (resolve, reject) {
				worker.onmessage = function (result) {
					var data = result.data;
					resolve(data);
					worker.terminate();
				};
				worker.onerror = function (err) {
					reject(err);
					worker.terminate();
				};
			});
		},
		triggerEvent: function (element, eventType, detail) {
			return element.dispatchEvent(new CustomEvent(eventType, {detail: detail}));
		},
		uuid: function () {
			return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, function (c) {
				return (c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))).toString(16);
			});
		},
		getTimeFromDate: function (date) {
			return date.toTimeString().slice(0, 8);
		},
		getDaysDiffBetweenDates: function (dateInitial, dateFinal) {
			return (dateFinal - dateInitial) / (1000 * 3600 * 24);
		},
		average: function () {
			var nums = [],
				i = 0;
			for (; i < arguments.length; i += 1) {
				nums[i] = arguments[i];
			}
			return nums.reduce(function (acc, val) {
				return acc + val;
			}, 0) / nums.length;
		},
		median: function (array) {
			var mid = Math.floor(array.length / 2), nums = array.slice().sort(function (a, b) {
				return a - b;
			});
			return array.length % 2 !== 0 ? nums[mid] : (nums[mid - 1] + nums[mid]) / 2;
		},
		degreesToRads: function (deg) {
			return (deg * Math.PI) / 180.0;
		},
		radsToDegrees: function (rad) {
			return (rad * 180.0) / Math.PI;
		},
		randomIntArrayInRange: function (min, max, n) {
			n = n || 1;
			return Array.from({length: n}, function () {
				return Math.floor(Math.random() * (max - min + 1)) + min;
			});
		},
		randomIntegerInRange: function (min, max) {
			return Math.floor(Math.random() * (max - min + 1)) + min;
		},
		randomNumberInRange: function (min, max) {
			return Math.random() * (max - min) + min;
		},
		round: function (n, decimals) {
			decimals = decimals || 0;
			return Number(Math.round(Number(n + 'e' + decimals)) + 'e-' + decimals);
		},
		standardDeviation: function (arr, usePopulation) {
			usePopulation = !!usePopulation;
			var mean = arr.reduce(function (acc, val) {
				return acc + val;
			}, 0) / arr.length;
			return Math.sqrt(arr.reduce(function (acc, val) {
				return acc.concat(Math.pow((val - mean), 2));
			}, []).reduce(function (acc, val) {
				return acc + val;
			}, 0) / (arr.length - (usePopulation ? 0 : 1)));
		},
		flattenObject: function (obj, prefix) {
			prefix = prefix || '';
			return Object.keys(obj).reduce(function (acc, k) {
				var pre = prefix.length ? prefix + '.' : '';
				if (typeof obj[k] === 'object')
					Object.assign(acc, u.flattenObject(obj[k], pre + k));
				else
					acc[pre + k] = obj[k];
				return acc;
			}, {});
		},
		invertKeyValues: function (obj, fn) {
			return Object.keys(obj).reduce(function (acc, key) {
				var val = fn ? fn(obj[key]) : obj[key];
				acc[val] = acc[val] || [];
				acc[val].push(key);
				return acc;
			}, {});
		},
		slugify: function (string) {
			var a = 'àáâäæãåāăąçćčđďèéêëēėęěğǵḧîïíīįìłḿñńǹňôöòóœøōõőṕŕřßśšşșťțûüùúūǘůűųẃẍÿýžźż·/_,:;',
				b = 'aaaaaaaaaacccddeeeeeeeegghiiiiiilmnnnnoooooooooprrsssssttuuuuuuuuuwxyyzzz------',
				p = new RegExp(a.split('').join('|'), 'g');
			return string.toString().toLowerCase()
				.replace(/\s+/g, '-') // Replace spaces with -
				.replace(p, function (c) {
					return b.charAt(a.indexOf(c));
				}) // Replace special characters
				.replace(/&/g, '-and-') // Replace & with 'and'
				.replace(/[^\w\-]+/g, '') // Remove all non-word characters
				.replace(/\-\-+/g, '-') // Replace multiple - with single -
				.replace(/^-+/, '') // Trim - from start of text
				.replace(/-+$/, ''); // Trim - from end of text
		},
		unflattenObject: function (obj) {
			return Object.keys(obj).reduce(function (acc, k) {
				if (k.indexOf('.') !== -1) {
					var keys = k.split('.'),
						dict = Object(JSON.parse('{' +
							keys.map(function (v, i) {
								return (i !== keys.length - 1 ? '"' + v + '":{' : '"' + v + '":');
							}).join('') +
							obj[k] +
							'}'.repeat(keys.length)));
					Object.assign(acc, dict);
				} else {
					acc[k] = obj[k];
				}
				return acc;
			}, {});
		},
		stripHTMLTags: function (str) {
			return str.replace(/<[^>]*>/g, '');
		},
		toCamelCase: function (str) {
			var result = str &&
				str.match(/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+/g).map(
					function (x) {
						return x.slice(0, 1).toUpperCase() + x.slice(1).toLowerCase();
					}
				).join('');
			return result.slice(0, 1).toLowerCase() + result.slice(1);
		},
		getCookie: function (name) {
			var values = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
			return values ? values[2] : null;
		},
		setCookie: function (name, value, days) {
			var newDate = new Date;
			newDate.setTime(newDate.getTime() + 24 * 60 * 60 * 1000 * days);
			document.cookie = name + '=' + value + ';path=/;expires=' + newDate.toUTCString();
		},
		removeCookie: function (name) {
			u.setCookie(name, '', -1);
		},
		removeElement: function (element) {
			element.parentNode.removeChild(element);
		},
		scrambleColors: function () {
			var getRandomInt = function (max) {
				return Math.floor(Math.random() * Math.floor(max));
			}, getRandomRGBA = function () {
				return 'rgba(' + getRandomInt(256) + ', ' + getRandomInt(256) + ', ' + getRandomInt(256) + ', 1.0)';
			};
			document.querySelectorAll('*').forEach(function (elm, index) {
				elm.style.backgroundColor = getRandomRGBA();
			});
		},
	};
	return u;
})();
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
var Djangoutils = {};
Djangoutils.Raw = {};
Djangoutils.Raw.EditTest = (function () {
	var r = {
	}, u = {
		initialize: function () {
		}
	};
	return u;
})();
Djangoutils.Raw.EditTest.initialize();