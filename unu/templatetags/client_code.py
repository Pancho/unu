import logging


from django import template
from django.utils import safestring
from django.conf import settings


register = template.Library()
logger = logging.getLogger(__name__)
SCRIPT = safestring.mark_safe('''
		<script>
			var optimize = function () {
				var cssFileUrl = document.getElementById('locator-css').getAttribute('src'),
					jsFileUrl = document.getElementById('locator-js').getAttribute('src'),
					jsRegexes = [/classList.add\(\'(.*?)\'\)/gi, /classList.toggle\(\'(.*?)\'\)/gi],
					jsHTMLRegex = /class\=\"(.*?)\"/gi,
					jsIncludeRegex = /\/\* CSS\: (.*?)\*\//gi,
					lazyStyles = [],
					selectorContainsAny = function (selector) {
						var result = false;
						lazyStyles.forEach(function (cssClass) {
							if (selector.indexOf(cssClass) !== -1) {
								result = true;
							}
						});
						return result;
					},
					stripPseudoClasses = function (selector) {
						var classes = [
							':active',
							':checked',
							':hover',
							':disabled',
							':required',
							':last-child',
							':first-child',
							':link',
							':not',
							':focus',
							':visited',
						], result = selector;

						classes.forEach(function (pseudoClass, index) {
							result = result.split(pseudoClass)[0];
						});

						if (result === '') {
							result = selector;
						}

						return result;
					},
					trimRules = function (rulesList) {
						var result = [];

						Object.keys(rulesList).forEach(function (key, index) {
							var rule = rulesList[key],
								innerRules = [],
								selector = '';

							if (rule.type === 1) {
								if (rule.selectorText.indexOf('fa-') !== -1) {
									selector = rule.selectorText.split(':')[0];

									if (selector === '') {
										selector = rule.selectorText;
									}
								} else {
									selector = stripPseudoClasses(rule.selectorText);
								}
								if ((document.querySelectorAll(selector).length > 0 || selectorContainsAny(selector)) && rule.styleMap.size > 0) {
									result.push(rule.cssText);
								}
							} else if (rule.type === 4) {
								innerRules = trimRules(rule.cssRules);
								result.push('@media ' + rule.conditionText + ' {' + innerRules.join('') + '}');
							} else if (rule.type === 5 || rule.type === 7) {
								result.push(rule.cssText);
							}
						});

						return result;
					};

				fetch(jsFileUrl, {
					method: 'GET'
				}).then(function (response) {
					return response.text();
				}).then(function (text) {
					var codeMatch = jsHTMLRegex.exec(text),
						includeMatch = jsIncludeRegex.exec(text),
						build = '';

					while (codeMatch !== null) {
						codeMatch[1].split(' ').forEach(function (cssClass, index) {
							if (lazyStyles.indexOf(cssClass) === -1) {
								lazyStyles.push(cssClass);
							}
						});
						codeMatch = jsHTMLRegex.exec(text);
					}

					while (includeMatch !== null) {
						includeMatch[1].trim().split(' ').forEach(function (includeSelector, index) {
							build += (' ' + includeSelector.trim());
							if (lazyStyles.indexOf(build) === -1) {
								lazyStyles.push(build);
							}
						});
						build = '';
						includeMatch = jsIncludeRegex.exec(text);
					}


					jsRegexes.forEach(function (regex, index) {
						var match = regex.exec(text);

						while (match !== null) {
							match[1].split('\\',\\'').forEach(function (cssClass, index) {
								if (lazyStyles.indexOf(cssClass) === -1) {
									lazyStyles.push(cssClass);
								}
							});
							match = regex.exec(text);
						}
					});

					//
					Object.keys(document.styleSheets).forEach(function (sheetKey, index) {
						var sheet = document.styleSheets[sheetKey],
							rules = trimRules(sheet.rules),
							fileName = sheet.href.split('/dist/')[1].split('?v=')[0],
							contents = rules.join(''),
							body = new FormData(),
							url = '{% url 'unu:optimize_client_code' %}';

						body.append('cssFile', sheet.href.split('/dist/')[1].split('?v=')[0]);
						body.append('cssContent', contents);
						body.append('jsFile', jsFileUrl.split('/dist/')[1].split('?v=')[0]);
						body.append('jsContent', text);

						config = {
							method: 'POST',
							credentials: 'include',
							headers: {
								'Accept': 'application/json',
								'X-Requested-With': 'XMLHttpRequest'
							},
							body: body
						};

						return fetch(url, config).then(function (response) {
							return response.json();
						}).then(function (result) {
							var container = document.createElement('div');

							if (result.status === 'ok') {
								container.textContent = 'Static Files Optimized';
							} else if (result.status === 'compilationError') {
								container.textContent = 'Optimization of files failed. See application logs for details.';
							}

							container.style = 'position:fixed;background:black;color:yellow;font-size:20px;padding:10px;top:20px;right:20px;z-index:999999;';

							document.body.appendChild(container);

							setTimeout(function () {
								document.body.removeChild(container);
							}, 5000);
						});
					});
				});
			};

			document.addEventListener('DOMContentLoaded', function () {
				optimize();
			});
		</script>''')


@register.simple_tag
def optimize():
	if settings.DEBUG:
		script_template = template.Template(SCRIPT)
		return script_template.render(template.Context({}))
	else:
		return ''
