/**
 * @author eshim
 */
jQuery(document).ready(function() {
	
	
	
	
//CodeMirror initialization
	var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    lineWrapping: true,
    extraKeys: {"Ctrl-Space": "autocomplete"},
    mode: "python", //syntax highlighting
    onCursorActivity: function() {
    	editor.matchHighlight("CodeMirror-matchhighlight");
 	}, //match highlighting
    gutter: true, //space in the line numbers column
    matchbrackets: true,  //match brackets on hover
    autofocus: true, //focus on load
    extraKeys: {"Ctrl-Space" : "autocomplete"}
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
