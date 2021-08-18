$(document).ready(function()
{
$( "#addCollForm" ).submit(function( event ) {
var name = ($("#name").val());
var owner = ($("#owner").val());
event.preventDefault();

jQuery.ajax({
        url: '/collections_post_api',
        type: 'GET',
        dataType: 'json',
	data: {
		"name": name,
		"owner": owner
	},
        success : function(data){
	     if (data.results === "exists"){
	     $("#success").notify("Collection already exists", "fail");}
	     else{
	     $("#success").notify("Sucess", "success");
	     $("#name").val("")
	     $("#owner").val("")}
        }
    });


});


	
});
