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

function getData(url){
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
  		//console.log(xhr.status);
	  	if (xhr.readyState == 4) {
	  		if (xhr.status === 200){// 200 = OK
	    		//console.log('success');
	  			var resp = JSON.parse(xhr.responseText);
	    		drawFlow(resp);
	    	}else{
	    		console.log('fail');
	    	}
	    }
  	};
  	xhr.open('GET',url,true);
  	xhr.send(null);
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
getData('x.data');