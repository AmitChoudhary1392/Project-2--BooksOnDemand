
//intialize leaflet map of toronto
var torontoMap = L.map('mapid').setView([43.653, -79.383], 13);


//intialize tile layer to do api call
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    accessToken: 'api_key'
}).addTo(torontoMap);


//creating function to map the book location whenver search function is called with d3 on click function or something
function mapBook() {
    /* data route */
  var url = "/api/findbook";
  d3.json(url).then(function(response) {
	
    console.log(response);

    var bookData = response;
	var marker = L.marker([latbook, lngbook]).addTo(torontoMap)
	
	
  };
	
	

	
	