

/**
 * @author eshim
 */


var oTable;
var giRedraw = false;

jQuery(document).ready(function() {
	
	
	//This will initialize the datatable plugin
	oTable = $("#sortTable").dataTable({
		//Changes the text of the initiallized features
		"oLanguage": {
			"sSearch": "",
			"sInfoEmpty": "No entries to show",
			"sZeroRecords": "No results to display"
		},
		
		"iDisplayLength": 20,
	
		//sets up the DOM for the table
		"sDom" : '<"top" fp>rt<"bottom" ip>',
		
		//Disables the user's ability to set table results length
		"bLengthChange": false,
		//sort all headers but submissions in desc order.
		"aaSorting": [[0,"asc"],[1,"asc"],[2,"asc"],[3,"asc"],[4,"desc"],[5,"asc"]]
	});
	
	//Sets the placeholder text for the Search bar
	$('.dataTables_filter input').attr("placeholder", "Enter filter terms here");
	
	//sets width/margin of dataTable wrapper
	$('.dataTables_wrapper').css({
		'margin-left': 'auto',
		'margin-right': 'auto',
		'width': '500px'
		});
	 
	// Add a click handler to the rows - this could be used as a callback 
	$("tbody").click(function(event) {
		$(oTable.fnSettings().aoData).each(function (){
			$(this.nTr).removeClass('selected');
		});
		$(event.target.parentNode).addClass('selected');
	});


}); // Ends ready(function()

function fnGetSelected( oTableLocal )
{
	var aReturn = new Array();
	var aTrs = oTableLocal.fnGetNodes();
	
	for ( var i=0 ; i<aTrs.length ; i++ )
	{
		if ( $(aTrs[i]).hasClass('selected') )
		{
			aReturn.push( aTrs[i] );
		}
	}
	return aReturn;
}