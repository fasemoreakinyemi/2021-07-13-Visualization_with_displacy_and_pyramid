$(document).ready(function()
{


window.load = check_argument()

function check_argument(){
	var route = location.href.split("/")[location.href.split("/").length - 2];
	if (route == "retrieve"){
		var id = location.href.split("/")[location.href.split("/").length - 1];
		load_input(id)
	}

}

function load_input(id){

jQuery.ajax({
        url: '/search_api',
        type: 'GET',
        dataType: 'json',
	data: {
		"articleId": id
	},
        success : function(data){
             	articles = JSON.parse(data.results)
		title = articles["liv"]["orig_data"]["TITLE"]
		abstracts = articles["liv"]["orig_data"]["ABSTRACT"]
             	$("#title").val(title) 
             	$("#abstract").val(abstracts)
        }
    });





}


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


$( "#search_form" ).submit(function( event ) {
var payload = {};
var search = ($("#search_input").val());
event.preventDefault();

jQuery.ajax({
        url: '/search_api',
        type: 'GET',
        dataType: 'json',
	data: {
		"search": search
	},
        success : display_results
    });


});

function display_results(data){
	     console.log( Object.keys( JSON.parse(data.results)).length )
             articles = JSON.parse(data.results)
	     var container = document.createElement("div")
	     container.className = "container"
	     articles.map(function(rows){
		     var card = create_card(rows)
		     container.append(card)
		  //   var doi = rows["liv"]["orig_data"]["DOI"]
		  //   var year = rows["liv"]["orig_data"]["PUBLYEAR"]
		  //   var volume = rows["liv"]["orig_data"]["VOLUME"]
		  //   var issue = rows["liv"]["orig_data"]["ISSUE"]
		  //   var pages = rows["liv"]["orig_data"]["PAGES"]
		  //   console.log(abstracts)
	     })
             $("#result").html(container)

};
	     

function create_card(rows){
	var card = document.createElement("div")
	card.className = "card my-5"

	var cardHeader = document.createElement("div")
        var authors = rows["liv"]["orig_data"]["AUTHOR"]
	cardHeader.className = "card-header"
	cardHeader.innerText = String(authors)

	var cardBody = document.createElement("div")
	cardBody.className = "card-body"

	var cardTitle = document.createElement("h5")
	var title = rows["liv"]["orig_data"]["TITLE"]
	cardTitle.className = "card-title"
	cardTitle.innerText = String(title)
	cardBody.append(cardTitle)
	
	var cardText = document.createElement("p")
	var abstracts = rows["liv"]["orig_data"]["ABSTRACT"]
	cardText.className = "card-text"
	cardText.innerHTML = String(abstracts)
	cardBody.append(cardText)
	console.log(abstracts)




	var cardFooter = document.createElement("div")
	var journal = rows["liv"]["orig_data"]["SOURCE"]
	cardFooter.className = "card-footer"
	cardFooter.innerText = String(journal)
	
	var cardLink = document.createElement("a")
	var id  = rows["_id"]["$oid"]
	cardLink.className = "btn btn-primary"
	cardLink.href = "/retrieve/" + id
	cardLink.innerText = "Analyze text"
	cardBody.append(cardLink)

	card.append(cardHeader)
	card.append(cardBody)
	card.append(cardFooter)

	return card
}


//<div class="card text-center">
//  <div class="card-header">
//    Featured
//  </div>
//  <div class="card-body">
//    <h5 class="card-title">Special title treatment</h5>
//    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
//    <a href="#" class="btn btn-primary">Go somewhere</a>
//  </div>
//  <div class="card-footer text-muted">
//    2 days ago
//  </div>
//</div>
	
});
