$(document).ready(function()
{

$( "#retrieve_entities" ).submit(function( event ) {
var payload = {};
var title = ($("#title").val());
var abst = ($("#abstract").val());
var model = ($("#model option:selected").val());
event.preventDefault();

jQuery.ajax({
        url: '/retrieve_api',
        type: 'GET',
        dataType: 'json',
	data: {
		"title": title,
		"abstract": abst,
		"model": model
	},
        success : function(data){
             $("#result").html(data.title)
        }
    });


});

function load_entities(data){
	$("#result").html(data)
}
});
