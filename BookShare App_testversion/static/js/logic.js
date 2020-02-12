// An array of books and their location
var books_index = [
    {
      name: "Harry Potter and the Order of Pheonix",
      location: [42.651, -77.347]
    },
    {
      name: "Da Vinci Code",
      location: [41.651, -72.347]
    },
    {
      name: "How to kill a mockingbird",
      location: [39.651, -78.347]
    },
    {
      name: "The Alchemist",
      location: [44.651, -79.347]
    }
  ];
  
  // An array which will be used to store created bookMarkers
  var bookMarkers = [];
  
  for (var i = 0; i < books_index.length; i++) {
    // loop through the cities array, create a new marker, push it to the cityMarkers array
    bookMarkers.push(
      L.marker(books_index[i].location).bindPopup("<h1>" + books_index[i].name + "</h1>")
    );
  }
  
  // Add all the cityMarkers to a new layer group.
  // Now we can handle them as one group instead of referencing each individually
  var cityLayer = L.layerGroup(bookMarkers);
  
  // Define variables for our tile layers
  var light = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.light",
    accessToken: API_KEY
  });
  
  var dark = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.dark",
    accessToken: API_KEY
  });
  
  // Only one base layer can be shown at a time
  var baseMaps = {
    Light: light,
    Dark: dark
  };
  
  // Overlays that may be toggled on or off
  var overlayMaps = {
    Cities: cityLayer
  };
  
  // Create map object and set default layers
  var myMap = L.map("map", {
    center: [43.651, -79.347],
    zoom: 7,
    layers: [light, cityLayer]
  });
  
  // Pass our map layers into our layer control
  // Add the layer control to the map
  L.control.layers(baseMaps, overlayMaps).addTo(myMap);
  