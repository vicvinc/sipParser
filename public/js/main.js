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
  	xhr.setRequestHeader("Content-Type", "multipart/form-data");
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
function uploadAndSubmit() {
	var form = document.getElementById('file').files;
	var fData = new FormData();
	if ( form.length > 0 ) {
		var file = form[0];
		fData.append(file.name, file);
		var reader = new FileReader();
		reader.onloadstart = function() {
			console.log("onloadstart");
			
		document.getElementById("bytesTotal").textContent = file.size;
		}
		
		reader.onprogress = function(p) {
			console.log("onprogress");
			document.getElementById("bytesRead").textContent = p.loaded;
		}
		
		reader.onload = function() {
			console.log("load complete");
		}
		
		reader.onloadend = function() {
			if (reader.error) {
				console.log(reader.error);
			} else {
				document.getElementById("bytesRead").textContent = file.size;
				var xhr = new XMLHttpRequest();
				xhr.open(/* method */ "POST", /* target url */ "upload?fileName=" + file.name /*, async, default to true */);
		  		xhr.overrideMimeType("application/octet-stream");
				//xhr.send(reader.result);
				xhr.send(fData);
				xhr.onreadystatechange = function() {
					if (xhr.readyState == 4) {
						if (xhr.status == 200) {
							console.log("upload complete");
							console.log("response: " + xhr.responseText);
						}
					}
				}
			}
		}
		reader.readAsBinaryString(file);
	}
	else{
		alert ("Please choose a file.");
	}
}
buildMessage : function(elements, boundary) {
    var CRLF = "\r\n";
    var parts = [];

    elements.forEach(function(element, index, all) {
        var part = "";
        var type = "TEXT";

        if (element.nodeName.toUpperCase() === "INPUT") {
            type = element.getAttribute("type").toUpperCase();
        }

        if (type === "FILE" && element.files.length > 0) {
            var fieldName = element.name;
            var fileName = element.files[0].fileName;

            /*
             * Content-Disposition header contains name of the field
             * used to upload the file and also the name of the file as
             * it was on the user's computer.
             */
            part += 'Content-Disposition: form-data; ';
            part += 'name="' + fieldName + '"; ';
            part += 'filename="'+ fileName + '"' + CRLF;

            /*
             * Content-Type header contains the mime-type of the file
             * to send. Although we could build a map of mime-types
             * that match certain file extensions, we'll take the easy
             * approach and send a general binary header:
             * application/octet-stream
             */
            part += "Content-Type: application/octet-stream";
            part += CRLF + CRLF; // marks end of the headers part

            /*
             * File contents read as binary data, obviously
             */
            part += element.files[0].getAsBinary() + CRLF;
       } else {
            /*
             * In case of non-files fields, Content-Disposition
             * contains only the name of the field holding the data.
             */
            part += 'Content-Disposition: form-data; ';
            part += 'name="' + element.name + '"' + CRLF + CRLF;

            /*
             * Field value
             */
            part += element.value + CRLF;
       }

       parts.push(part);
    });

    var request = "--" + boundary + CRLF;
        request+= parts.join("--" + boundary + CRLF);
        request+= "--" + boundary + "--" + CRLF;

    return request;
}
(function listener(){
	var subt = document.getElementById('fileSubmit');
	document.getElementById('fileSubmit').addEventListener('click', function(){
		//var forms = document.forms[];
		uploadAndSubmit();
		//postData('upload', d);
	});
}());
