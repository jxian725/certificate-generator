(function() {
	"use strict";
	var	$body = document.querySelector('body');
	!function(){function t(t){this.el=t;for(var n=t.className.replace(/^\s+|\s+$/g,"").split(/\s+/),i=0;i<n.length;i++)e.call(this,n[i])}function n(t,n,i){Object.defineProperty?Object.defineProperty(t,n,{get:i}):t.__defineGetter__(n,i)}if(!("undefined"==typeof window.Element||"classList"in document.documentElement)){var i=Array.prototype,e=i.push,s=i.splice,o=i.join;t.prototype={add:function(t){this.contains(t)||(e.call(this,t),this.el.className=this.toString())},contains:function(t){return-1!=this.el.className.indexOf(t)},item:function(t){return this[t]||null},remove:function(t){if(this.contains(t)){for(var n=0;n<this.length&&this[n]!=t;n++);s.call(this,n,1),this.el.className=this.toString()}},toString:function(){return o.call(this," ")},toggle:function(t){return this.contains(t)?this.remove(t):this.add(t),this.contains(t)}},window.DOMTokenList=t,n(Element.prototype,"classList",function(){return new t(this)})}}();
	window.canUse=function(p){if(!window._canUse)window._canUse=document.createElement("div");var e=window._canUse.style,up=p.charAt(0).toUpperCase()+p.slice(1);return p in e||"Moz"+up in e||"Webkit"+up in e||"O"+up in e||"ms"+up in e};
	(function(){if("addEventListener"in window)return;window.addEventListener=function(type,f){window.attachEvent("on"+type,f)}})();
	window.addEventListener('load', function() {
		window.setTimeout(function() {
			$body.classList.remove('is-preload');
		}, 100);
	});
	(function() {
		var settings = {
			images: {
				'/assets/images/bg01.jpg': 'center',
				'/assets/images/bg02.jpg': 'center',
				'/assets/images/bg03.jpg': 'center'
			},
			delay: 6000
		};
		var	pos = 0, lastPos = 0, $wrapper, $bgs = [], $bg, k, v;
		$wrapper = document.createElement('div');
		$wrapper.id = 'bg';
		$body.appendChild($wrapper);

		for (k in settings.images) {
			$bg = document.createElement('div');
			$bg.style.backgroundImage = 'url("' + k + '")';
			$bg.style.backgroundPosition = settings.images[k];
			$wrapper.appendChild($bg);
			$bgs.push($bg);
		}
		$bgs[pos].classList.add('visible');
		$bgs[pos].classList.add('top');
		if ($bgs.length == 1 ||	!canUse('transition')) return;
		window.setInterval(function() {
			lastPos = pos;
			pos++;
			if (pos >= $bgs.length) pos = 0;
			$bgs[lastPos].classList.remove('top');
			$bgs[pos].classList.add('visible');
			$bgs[pos].classList.add('top');
			window.setTimeout(function() {
				$bgs[lastPos].classList.remove('visible');
			}, settings.delay / 2);
		}, settings.delay);
	})();

	(function() {
		var $form = document.querySelectorAll('#query-form')[0],
			$submit = document.querySelectorAll('#query-form input[type="submit"]')[0],
			$message;
		if (!('addEventListener' in $form)) return;
		$message = document.createElement('span');
		$message.classList.add('message');
		$form.appendChild($message);
		$message._show = function(type, text) {
			$message.innerHTML = text;
			$message.classList.add(type);
			$message.classList.add('visible');
			window.setTimeout(function() {
				$message._hide();
			}, 3000);
		};
		$message._hide = function() {
			$message.classList.remove('visible');
		};

		$form.addEventListener('submit', function(event) {
			event.stopPropagation();
			event.preventDefault();
			$message._hide();
			$submit.disabled = true;

			let country = document.getElementById("country").value;
			let query = (document.getElementById("query").value).trim();
			let queryPayload = "";

			if (country === "") {
				$message._show('failure', 'Please select your country/region.');
				$submit.disabled = false;
				return;
			} else if (query === ""){
				$message._show('failure', 'Please fill in with either one combination.');
				$submit.disabled = false;
				return;
			} else {
				if (query.length < 3) {
					$message._show('failure', 'Invalid combination.');
					$submit.disabled = false;
					return;
				} else {
					if (query.includes("@")) {
						queryPayload = `{"country":"${country}","email":"${query}"}`;	
					} else if (query.length >= 30 && !query.includes(" ")) {
						queryPayload = `{"country":"${country}","accountId":"${query}"}`;	
					} else {
						queryPayload = `{"country":"${country}","name":"${query}"}`;	
					}
					fetch("http://188.239.13.84/api/participant/query", {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
						},
						body: queryPayload,
					}).then(response => response.json()).then(result => {
						if (result.status === "success") {
							getCertificate(result.data);
						} else {
							$message._show('failure', 'No matching result found.');
							$submit.disabled = false;
							return;
						}
					}).catch(error => {
						console.error("Error:", error);
						$message._show('failure', 'Error. Please try again later.');
						$submit.disabled = false;
						return;
					});
				}
			}
		});

		function getCertificate(args){
			let modal = document.getElementById("certModal");
			let span = document.getElementsByClassName("certClose")[0];
			span.onclick = function() {
				modal.style.display = "none";
				document.getElementById("cert-frame").src = "";
				document.getElementById("download-icon").alt = "";
			}

			window.onclick = function(event) {
				if (event.target == modal) {
					modal.style.display = "none";
					document.getElementById("cert-frame").src = "";
					document.getElementById("download-icon").alt = "";
				}
			}
			fetch(`http://188.239.13.84/api/generate/${args.id}`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
			}).then(response => response.json()).then(result => {
				let objectURL = `data:image/png;base64,${result.blob}`;
				document.getElementById("cert-frame").src = objectURL;
				document.getElementById("download-icon").alt = result.url;
				$message._show('success', 'Certificate generated successfully.');
				$submit.disabled = false;
				modal.style.display = "block";
				return;
			}).catch(error => {
				console.error("Error:", error);
				$message._show('failure', 'Error. Please try again later2.');
				$submit.disabled = false;
				return;
			});

			let downloadBar = document.querySelectorAll('#certModal .action-bar')[0];
			downloadBar.onclick = function() {
				const a = document.createElement('a');
				a.href = document.getElementById("download-icon").alt;
				a.download = (a.href).split('/').pop();
				document.body.appendChild(a);
				a.click();
				document.body.removeChild(a);
			}
		}
	})();

	(function(){
		let modal = document.getElementById("hintModal");
		let btn = document.getElementById("viewGuide");
		let span = document.getElementsByClassName("close")[0];

		btn.onclick = function() {
			modal.style.display = "block";
		}

		span.onclick = function() {
			modal.style.display = "none";
		}

		window.onclick = function(event) {
			if (event.target == modal) {
				modal.style.display = "none";
			}
		}
	})();
})();

function viewImage(args){
	window.open(args.src, '_blank').focus();
}