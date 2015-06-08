/** js sequence diagrams 1.0.6
 *  http://bramp.github.io/js-sequence-diagrams/
 *  (c) 2012-2015 Andrew Brampton (bramp.net)
 *  @license Simplified BSD license.
 */
(function () {
	'use strict';
	/*global Diagram */

	/*> ../build/diagram-grammar.js */
	/*> ../fonts/daniel/daniel_700.font.js */
	/*> sequence-diagram.js */
	/*> jquery-plugin.js */

	// Taken from what underscore.js:
	// Establish the root object, `window` (`self`) in the browser, or `global` on the server.
	// We use `self` instead of `window` for `WebWorker` support.
	var root = (typeof self == 'object' && self.self == self && self) ||
		(typeof global == 'object' && global.global == global && global);

	// Export the Diagram object for **Node.js**, with
	// backwards-compatibility for their old module API. If we're in
	// the browser, add `Diagram` as a global object.
	if (typeof exports !== 'undefined') {
		if (typeof module !== 'undefined' && module.exports) {
			exports = module.exports = Diagram;
		}
		exports.Diagram = Diagram;
	} else {
		root.Diagram = Diagram;
	}
}());
/************************************************************************************/
/*              draw sequence diagram below                                         */
/************************************************************************************/

function postData(url, data){
	var xhr=null;
	if (window.XMLHttpRequest){// code for all new browsers
	  	xhr = new XMLHttpRequest();
	}else if(window.ActiveXObject){// code for IE5 and IE6
	  	xhr = new ActiveXObject('Microsoft.XMLHTTP');
	}
	if (xhr == null){
		return ;
	}
  	xhr.onreadystatechange = function(){
	  	if (xhr.readyState == 4) {
	  		if (xhr.status === 200){// 200 = OK
	  			var resp = JSON.parse(xhr.responseText);
	    		drawFlow(resp);
	    	}else{
	    		console.log('fail');
	    	}
	    }
  	};
	//xhr.sendAsBinary(data);
  	xhr.open('POST', url, true);
  	xhr.setRequestHeader('Content-Type', 'multipart/form-data');
  	xhr.send(data);
}

/**************************** draw function ********************************/

function drawFlow(respData){
	// console.log(respData);
	//console.log(typeof(respData));
	var dgm = '';
	for (x in respData){
		// console.log(x);
		// console.log(respData[x]);
		var msg = JSON.parse(respData[x]);
		// console.log(typeof(msg));
		// console.log(msg.msgFrom + '->' + msg.to);
		dgm = dgm + msg.msgFrom.replace(':','/') + 
			'->' + 
			msg.to.replace(':','/') + ': ' + 
			msg.method + ' ' + msg.statuscode + '\n';
	}
	var diagram = Diagram.parse(dgm);
		diagram.drawSVG('diagram', {theme: 'simple'});
	//diagram.drawSVG('diagram', {theme: 'simple'});
	// var diagram = Diagram.parse('A->B: Message');
	// diagram.drawSVG('diagram', {theme: 'simple'});
}

/***********************************************************************
             upload file and get parser response                      
************************************************************************/

function uploadAndSubmit() {
	var form = document.getElementById('file').files;
	var fData = new FormData();
	if ( form.length > 0 ) {
		var file = form[0];
		fData.append(file.name, file);
		var reader = new FileReader();
		reader.onloadstart = function() {
			// console.log('onloadstart');
			document.getElementById('bytesTotal').textContent = file.size;
		}
		
		reader.onprogress = function(p) {
			// console.log('onprogress');
			document.getElementById('bytesRead').textContent = p.loaded;
		}
		
		reader.onload = function() {
			// console.log('load complete');
		}
		
		reader.onloadend = function() {
			if (reader.error) {
				console.log(reader.error);
			} else {
				document.getElementById('bytesRead').textContent = file.size;
				var xhr = new XMLHttpRequest();
				xhr.open(/* method */ 'POST', /* target url */ 'upload?f=' + file.name /*, async, default to true */);
				xhr.send(fData);
				xhr.onreadystatechange = function() {
					if (xhr.readyState == 4) {
						if (xhr.status == 200) {
							var resp = JSON.parse(xhr.responseText);
	    					drawFlow(resp);
						}
					}
				}
			}
		}
		reader.readAsBinaryString(file);
	}
	else{
		alert ('Please choose a file.');
	}
}
(function listener(){
	var subt = document.getElementById('fileSubmit');
	document.getElementById('fileSubmit').addEventListener('click', function(){
		uploadAndSubmit();
	});
}());
