/*
 * @author eshim
 */

//coding in jQuery: what you want to happen, not how.



jQuery(document).ready(function() {
	
	// $(function() {
		// $( "#tabs" ).tabs();
	// });	
	
	//This will slide the submission field into view and expand the header 
	//so that the description is viewable when title is toggled
	$( ".taskHeader" ).click(function(){
		$(this).parent().find(".submissionField").toggle(300);
		$(this).toggleClass( "expand", 300 );
	});
	
	//This will make sure that tasksHeaderContainers without the class 
	//"toggleOpen" will be closed. Allows people w/ jscript on to see content
	$(".tasksContainerHeader:not(.toggleOpen)").addClass( "toggleClosed" ).next().hide();    
	
	//This will slide the tasks into view and move the other sections smoothly
	//when the taskContainerHeader is clicked 
	$( ".tasksContainerHeader" ).click(function() {
		if($(this).hasClass( "toggleOpen" )) {
			$(this).removeClass( "toggleOpen" ).addClass( "toggleClosed" ).next().slideUp( 300 );
		} else {
			$(this).removeClass( "toggleClosed" ).addClass( "toggleOpen" ).next().slideDown( 300 );
		}
	});
	
	
	
	
	
	
}); // Ends ready(function()

//Get the rows which are currently selected 




