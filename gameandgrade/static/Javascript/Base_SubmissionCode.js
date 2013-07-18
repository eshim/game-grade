/**
 * @author eshim
 */
jQuery(document).ready(function() {
	
	
	
	
//CodeMirror initialization
	var editor = CodeMirror.fromTextArea(document.getElementById("codeForm"), {
    lineNumbers: true,
    lineWrapping: true,
    extraKeys: {"Ctrl-Space": "autocomplete"},
    mode: "python", // syntax highlighting
    onCursorActivity: function() {
    	editor.matchHighlight("CodeMirror-matchhighlight");
 	}, // match highlighting
    gutter: true, // space in the line numbers column
    matchbrackets: true,  // match brackets on hover
    autofocus: true, // focus on load
    readOnly: true, // non-editable (until we can have them edit code)
    viewportMargin: Infinity // should resize based on window
	});
	
	var input = document.getElementById("select");

	document.getElementById("select").onchange = function (){
	    var theme = input.options[input.selectedIndex].innerHTML;
	    editor.setOption("theme", theme);
	}	
	var choice = document.location.search && document.location.search.slice(1);
	
	if (choice) {
	    input.value = choice;
	    editor.setOption("theme", choice);
	}

}); // Ends ready(function()

// function submitCode() {
		// //get the code
		// var code = document.getElementById("code").getValue();
		// //send code to server
		// //change the output field
		// var pylintOutput = {
			// target: '#submissionCode_pylintOutput',
			// beforeSubmit: function() {
				// $('')
			// }
		// }
// }

function tab(tab) {
	document.getElementById('tab1').style.display = 'none';
	document.getElementById('tab2').style.display = 'none';
	document.getElementById('li-tab1').setAttribute("class","");
	document.getElementById('li-tab2').setAttribute("class","");
	document.getElementById(tab).style.display = 'block'; //need this to redisplay the material
	document.getElementById(tab).style.display = '-moz-box';
	document.getElementById('li-'+tab).setAttribute("class", "active");
}
