'use strict';var k=function(){var g={a:{},I:'a span bdo em strong dfn code samp kbd var cite abbr acronym q sub sup tt i b big small u s strike font ins del pre address dt h1 h2 h3 h4 h5 h6'.split(' '),s:function(a,b){document.addEventListener(a,function(c){g.a[a].forEach(function(d){for(var f=c.target;f&&f!==document;f=f.parentNode)if(f.matches(d.i)){try{d.o.call(f,c)}catch(h){console.log(h)}break}})},!!b)},g:function(a,b,c){for(var d=Array(b+1).join(c),f=Array(b).join(c),h,l=0,m=a.children.length;l<
m;l+=1)-1===g.I.indexOf(a.children[l].tagName.toLowerCase())?(h=document.createTextNode('\n'+d),a.insertBefore(h,a.children[l]),g.g(a.children[l],b+1,c),a.lastElementChild===a.children[l]&&(h=document.createTextNode('\n'+f),a.appendChild(h))):(h=document.createTextNode('\n'+d),a.insertBefore(h,a.children[l]),h=document.createTextNode('\n'+f),a.appendChild(h));return a.innerHTML.replace(/^\s*$(?:\r\n?|\n)/gm,'')},l:{linear:function(a){return a},easeInQuad:function(a){return a*a},easeOutQuad:function(a){return a*
(2-a)},easeInOutQuad:function(a){return.5>a?2*a*a:-1+(4-2*a)*a},easeInCubic:function(a){return a*a*a},easeOutCubic:function(a){return--a*a*a+1},easeInOutCubic:function(a){return.5>a?4*a*a*a:(a-1)*(2*a-2)*(2*a-2)+1},easeInQuart:function(a){return a*a*a*a},easeOutQuart:function(a){return 1- --a*a*a*a},easeInOutQuart:function(a){return.5>a?8*a*a*a*a:1-8*--a*a*a*a},easeInQuint:function(a){return a*a*a*a*a},easeOutQuint:function(a){return 1+--a*a*a*a*a},easeInOutQuint:function(a){return.5>a?16*a*a*a*a*
a:1+16*--a*a*a*a*a}}},e={K:function(){},b:function(a,b,c,d,f){g.a[b]||(g.a[b]=[],g.s(b,f));g.a[b].push({i:a,J:d||'global',o:c})},ra:function(a,b,c){g.a[a].forEach(function(d,f){d.i===b&&d.J===c&&g.a[a].splice(f,1)})},scrollTo:function(a,b,c,d){function f(){var t=g.l[c](Math.min(1,(('now'in window.performance?performance.now():(new Date).getTime())-l)/b));window.scroll(0,Math.ceil(t*(p-h)+h));2>Math.abs(window.pageYOffset-p)?d():(n=r.offsetTop,p=Math.round(m-n<q?m-q:n),requestAnimationFrame(f))}var h=
window.pageYOffset,l='now'in window.performance?performance.now():(new Date).getTime(),m=Math.max(document.body.scrollHeight,document.body.offsetHeight,document.documentElement.clientHeight,document.documentElement.scrollHeight,document.documentElement.offsetHeight),q=window.innerHeight||document.documentElement.clientHeight||document.querySelector('body').clientHeight,r=document.querySelector(a),n=r.offsetTop,p=Math.round(m-n<q?m-q:n);b=b||200;c=c||'linear';d=d||e.K;'requestAnimationFrame'in window?
f():(window.scroll(0,p),d())},h:function(a){var b=[];Object.keys(a).forEach(function(c){b.push(encodeURIComponent(c)+'='+encodeURIComponent(a[c]))});return b.join('&')},get:function(a,b){var c=document.querySelector('body').dataset[a]||a;0===a.indexOf('/')&&(c=a);b=b||{};b.method='GET';return fetch(c,b)},L:function(a,b){var c=document.querySelector('body').dataset[a]||a;0===a.indexOf('/')&&(c=a);b=b||{};b.method='POST';b.credentials='include';b.headers||(b.headers={});b.headers.Accept||(b.headers.Accept=
'application/json');b.headers['X-Requested-With']||(b.headers['X-Requested-With']='XMLHttpRequest');return fetch(c,b)},da:function(a,b){var c=document.createElement('div');a=a.replace(/\n/g,'').replace(/[\t ]+</g,'<').replace(/>[\t ]+</g,'><').replace(/>[\t ]+$/g,'>');c.innerHTML=a.trim();return g.g(c,0,b||'\t')},Ca:function(){var a=document.querySelector('body');return window.innerWidth||document.documentElement.clientWidth||a.clientWidth},W:function(a,b,c){var d=null;return function(f){var h=this,
l=c&&!d;clearTimeout(d);d=setTimeout(function(){d=null;c||a.apply(h,[f])},b);l&&a.apply(h,[f])}},S:function(a,b){b=b||',';return a.map(function(c){return c.map(function(d){return isNaN(d)?'\\'+d.replace(/"/g,'""')+'\\':d}).join(b)}).join('\n')},U:function(a,b){return Array.from({length:Math.ceil(a.length/b)},function(c,d){return a.slice(d*b,d*b+b)})},V:function(a,b){return a.map('function'===typeof b?b:function(c){return c[b]}).reduce(function(c,d){c[d]=(c[d]||0)+1;return c},{})},j:function(a){return[].concat.apply([],
a.map(function(b){return Array.isArray(b)?e.j(b):b}))},ca:function(a,b){return a.map('function'===typeof b?b:function(c){return c[b]}).reduce(function(c,d,f){c[d]=(c[d]||[]).concat(a[f]);return c},{})},P:function(a,b,c){c=c||',';return[b.join(c)].concat(a.map(function(d){return b.reduce(function(f,h){return''+f+(f.length?c:'')+'"'+(d[h]?d[h]:'')+'"'},'')})).join('\n')},la:function(a){return a[Math.floor(Math.random()*a.length)]},ua:function(a){for(var b=a.slice(0),c=b.length,d;c;)d=Math.floor(Math.random()*
--c),a=[b[d],b[c]],b[c]=a[0],b[d]=a[1];return b},Aa:function(a,b){return Array.from(new Set(a.concat(b)))},createElement:function(a){var b=document.createElement('div');b.innerHTML=a;return b.firstElementChild},Z:function(a){var b=document.createElement('div');b.appendChild(a);return b.innerHTML},ha:function(){return/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)},Y:function(a,b){return a!==b&&a.contains(b)},ea:function(a,b){return a.insertAdjacentHTML('afterend',
b)},insertBefore:function(a,b){return a.insertAdjacentHTML('beforebegin',b)},fa:function(a,b){return a.insertAdjacentHTML('beforeend',b)},ja:function(a,b,c){var d=new MutationObserver(function(f){return f.forEach(function(h){return b(h)})});d.observe(a,Object.assign({childList:!0,attributes:!0,attributeOldValue:!0,characterData:!0,characterDataOldValue:!0,subtree:!0},c));return d},sa:function(a){var b=new Worker(URL.createObjectURL(new Blob(['postMessage(('+a+')());'])));return new Promise(function(c,
d){b.onmessage=function(f){c(f.data);b.terminate()};b.onerror=function(f){d(f);b.terminate()}})},ya:function(a,b,c){return a.dispatchEvent(new CustomEvent(b,{detail:c}))},Ba:function(){return'10000000-1000-4000-8000-100000000000'.replace(/[018]/g,function(a){return(a^crypto.getRandomValues(new Uint8Array(1))[0]&15>>a/4).toString(16)})},ba:function(a){return a.toTimeString().slice(0,8)},aa:function(a,b){return(b-a)/864E5},T:function(){for(var a=[],b=0;b<arguments.length;b+=1)a[b]=arguments[b];return a.reduce(function(c,
d){return c+d},0)/a.length},ia:function(a){var b=Math.floor(a.length/2),c=a.slice().sort(function(d,f){return d-f});return 0!==a.length%2?c[b]:(c[b-1]+c[b])/2},X:function(a){return a*Math.PI/180},ka:function(a){return 180*a/Math.PI},ma:function(a,b,c){return Array.from({length:c||1},function(){return Math.floor(Math.random()*(b-a+1))+a})},na:function(a,b){return Math.floor(Math.random()*(b-a+1))+a},oa:function(a,b){return Math.random()*(b-a)+a},round:function(a,b){b=b||0;return Number(Math.round(Number(a+
'e'+b))+'e-'+b)},va:function(a,b){b=!!b;var c=a.reduce(function(d,f){return d+f},0)/a.length;return Math.sqrt(a.reduce(function(d,f){return d.concat(Math.pow(f-c,2))},[]).reduce(function(d,f){return d+f},0)/(a.length-(b?0:1)))},m:function(a,b){b=b||'';return Object.keys(a).reduce(function(c,d){var f=b.length?b+'.':'';'object'===typeof a[d]?Object.assign(c,e.m(a[d],f+d)):c[f+d]=a[d];return c},{})},ga:function(a,b){return Object.keys(a).reduce(function(c,d){var f=b?b(a[d]):a[d];c[f]=c[f]||[];c[f].push(d);
return c},{})},O:function(a){return a.toString().toLowerCase().replace(/\s+/g,'-').replace(/\u00e0|\u00e1|\u00e2|\u00e4|\u00e6|\u00e3|\u00e5|\u0101|\u0103|\u0105|\u00e7|\u0107|\u010d|\u0111|\u010f|\u00e8|\u00e9|\u00ea|\u00eb|\u0113|\u0117|\u0119|\u011b|\u011f|\u01f5|\u1e27|\u00ee|\u00ef|\u00ed|\u012b|\u012f|\u00ec|\u0142|\u1e3f|\u00f1|\u0144|\u01f9|\u0148|\u00f4|\u00f6|\u00f2|\u00f3|\u0153|\u00f8|\u014d|\u00f5|\u0151|\u1e55|\u0155|\u0159|\u00df|\u015b|\u0161|\u015f|\u0219|\u0165|\u021b|\u00fb|\u00fc|\u00f9|\u00fa|\u016b|\u01d8|\u016f|\u0171|\u0173|\u1e83|\u1e8d|\u00ff|\u00fd|\u017e|\u017a|\u017c|\u00b7|\/|_|,|:|;/g,
function(b){return'aaaaaaaaaacccddeeeeeeeegghiiiiiilmnnnnoooooooooprrsssssttuuuuuuuuuwxyyzzz------'.charAt('\u00e0\u00e1\u00e2\u00e4\u00e6\u00e3\u00e5\u0101\u0103\u0105\u00e7\u0107\u010d\u0111\u010f\u00e8\u00e9\u00ea\u00eb\u0113\u0117\u0119\u011b\u011f\u01f5\u1e27\u00ee\u00ef\u00ed\u012b\u012f\u00ec\u0142\u1e3f\u00f1\u0144\u01f9\u0148\u00f4\u00f6\u00f2\u00f3\u0153\u00f8\u014d\u00f5\u0151\u1e55\u0155\u0159\u00df\u015b\u0161\u015f\u0219\u0165\u021b\u00fb\u00fc\u00f9\u00fa\u016b\u01d8\u016f\u0171\u0173\u1e83\u1e8d\u00ff\u00fd\u017e\u017a\u017c\u00b7/_,:;'.indexOf(b))}).replace(/&/g,
'-and-').replace(/[^\w\-]+/g,'').replace(/\-\-+/g,'-').replace(/^-+/,'').replace(/-+$/,'')},za:function(a){return Object.keys(a).reduce(function(b,c){if(-1!==c.indexOf('.')){var d=c.split('.');c=Object(JSON.parse('{'+d.map(function(f,h){return h!==d.length-1?'"'+f+'":{':'"'+f+'":'}).join('')+a[c]+'}'.repeat(d.length)));Object.assign(b,c)}else b[c]=a[c];return b},{})},wa:function(a){return a.replace(/<[^>]*>/g,'')},xa:function(a){a=a&&a.match(/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+/g).map(function(b){return b.slice(0,
1).toUpperCase()+b.slice(1).toLowerCase()}).join('');return a.slice(0,1).toLowerCase()+a.slice(1)},$:function(a){return(a=document.cookie.match('(^|;) ?'+a+'=([^;]*)(;|$)'))?a[2]:null},M:function(a,b,c){var d=new Date;d.setTime(d.getTime()+864E5*c);document.cookie=a+'='+b+';path=/;expires='+d.toUTCString()},pa:function(a){e.M(a,'',-1)},qa:function(a){a.parentNode.removeChild(a)},ta:function(){function a(b){return Math.floor(Math.random()*Math.floor(b))}document.querySelectorAll('*').forEach(function(b){b.style.backgroundColor=
'rgba('+a(256)+', '+a(256)+', '+a(256)+', 1.0)'})}};return e}(),u=function(){var g={H:function(){k.b('.box-tabbed .tabs li','click',function(e){e.preventDefault();this.closest('.box').querySelectorAll('.tabs li').forEach(function(a){a.classList.remove('selected','border-blue-50','bg-white')});this.closest('.box').querySelectorAll('.tabs-content li').forEach(function(a){a.style.display='none'});this.classList.add('selected','border-blue-50','bg-white');document.querySelector('#'+this.dataset.target).style.display=
'block'},'tabbed-boxes')},C:function(){k.b('#notifications .close','click',function(e){e.preventDefault();this.closest('li').style.display='none';this.closest('li').parentNode.removeChild(this)},'notifications')},N:function(e,a,b){e.style['grid-template-rows']='repeat('+a+', 1fr)';e.style['grid-template-columns']='repeat('+b+', 1fr)'},v:function(){document.querySelectorAll('[data-grid]').forEach(function(e){var a=e.dataset.grid;if(a){var b=a.split('/');a=b[0];b=b[1];g.N(e,a,b)}});document.querySelectorAll('[data-rows]').forEach(function(e){e.style['grid-row']=
e.dataset.rows});document.querySelectorAll('[data-columns]').forEach(function(e){e.style['grid-column']=e.dataset.columns})}};return{c:function(){g.v();g.H();g.C()}}}();
(function(){var g={A:function(){var e=null;'IntersectionObserver'in window?(e=new IntersectionObserver(function(a){a.forEach(function(b){var c;0<b.intersectionRatio&&(e.unobserve(b.target),b=b.target,c=b.dataset.src)&&(0<=c.indexOf('-2x.')?(b.setAttribute('srcset',c),b.setAttribute('src',c.replace('-2x',''))):b.setAttribute('src',c))})},{rootMargin:'50px 0px',threshold:.01}),document.querySelectorAll('img:not(.preload)').forEach(function(a){e.observe(a)})):document.querySelectorAll('img:not(.preload)').forEach(function(a){var b=
a.dataset.src;0<=b.indexOf('-2x.')?(a.setAttribute('srcset',b),a.setAttribute('src',b.replace('-2x',''))):a.setAttribute('src',b)})}};return{c:function(){g.A()}}})().c();
(function(){var g={D:function(){document.querySelectorAll('.populate-with-apps').forEach(function(e){var a=e.dataset.getAppsUrl;e.dataset.modelsOnly&&(a+='?'+k.h({Da:!0}));fetch(a).then(function(b){return b.json()}).then(function(b){if('ok'===b.status){for(;e.lastElementChild;)e.removeChild(e.lastElementChild);b.apps.forEach(function(c){e.appendChild(k.createElement('<option value="'+c+'">'+c+'</option>'))})}})})},f:function(e){var a=document.querySelector(e.dataset.ref),b=e.dataset.getModelsUrl+
'?'+k.h({R:a.value});0===a.querySelectorAll('option').length?setTimeout(function(){g.f(e)},1E3):fetch(b).then(function(c){return c.json()}).then(function(c){if('ok'===c.status){for(;e.lastElementChild;)e.removeChild(e.lastElementChild);c.models.forEach(function(d){e.appendChild(k.createElement('<option value="'+d+'">'+d+'</option>'))})}})},F:function(){document.querySelectorAll('.populate-with-models').forEach(function(e){g.f(e)});k.b('.populate-with-apps','change',function(){document.querySelectorAll('.populate-with-models').forEach(function(e){g.f(e)})})},
B:function(){k.b('.live-slugify','input',function(e){var a=e.target.closest('li');a.querySelectorAll('.live-slug').forEach(function(b){a.removeChild(b)});a.append(k.createElement('<p class="live-slug">'+k.O(e.target.value)+'</p>'))})},u:function(){k.b('form','submit',function(e){e.preventDefault();k.L(e.target.getAttribute('action'),{body:new FormData(e.target)}).then(function(a){return a.json()}).then(function(a){for(var b=document.getElementById('log');b.lastElementChild;)b.removeChild(b.lastElementChild);
'ok'===a.status&&a.log.forEach(function(c,d){b.appendChild(k.createElement('<li class="border-grey-10">['+d+']: '+c+'</li>'))})})})},G:function(){document.querySelectorAll('.populate-urls').forEach(function(e){fetch(e.dataset.getUrls).then(function(a){return a.json()}).then(function(a){if('ok'===a.status){for(;e.lastElementChild;)e.removeChild(e.lastElementChild);a.urlNames.forEach(function(b){e.appendChild(k.createElement('<option value="'+b+'">'+b+'</option>'))})}})})}};return{c:function(){u.c();
g.D();g.F();g.G();g.B();g.u()}}})().c();