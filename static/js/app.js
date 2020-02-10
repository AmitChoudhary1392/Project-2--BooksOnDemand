//function to create table header for search results
function generateTableHead(table, data) {
    var thead = table.createTHead();
    var row = thead.insertRow();
    data.forEach((key)=> {
        var cell = row.insertCell();
        cell.innerHTML= key;
    })
  }
  
//function to create table rows for search results
function generateTable(table, data) {

data.forEach((element)=> {
    var row = table.insertRow();
    Object.entries(element).forEach(([key,value])=> {
    
    var cell = row.insertCell();
    if (key=='title'){
    cell.innerHTML= value.link('/send')
    }
    if (key=='image_url'){
        var img= document.createElement('img');
        img.src='value';
        cell.appendChild(img); 
            }
    else {
        cell.innerHTML= value
    }
    })
})
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////       uSer book search results table display
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//create bookresults table--- display results when user is searching for the books
var url = "/api/findbook";
d3.json(url).then(function(response) {

    console.log(response);
    
    var table = document.getElementById("get-books");
    var data = Object.keys(response[0]);
    
    generateTable(table, response);         //call function to generate table
    generateTableHead(table, data);         //call fucntion to add table header
   
});

//select book results to redirect to display owner details and Locations

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////       Owner book search results table display
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//create bookresults table--- display results when owner is searching for the books and adding details
var url2 = "/api/findbook_owner";
d3.json(url).then(function(response) {

    console.log(response);
    
    var table = document.getElementById("get-books");
    var data = Object.keys(response[0]);

    generateTableHead(table, data);     //call function to generate table
    generateTable(table, response);     //call fucntion to add table header
    
   
});

//select book results to redirect to enter owner details


 /*  var mountains = [
    { name: "Monte Falco", height: 1658, place: "Parco Foreste Casentinesi" },
    { name: "Monte Falterona", height: 1654, place: "Parco Foreste Casentinesi" },
    { name: "Poggio Scali", height: 1520, place: "Parco Foreste Casentinesi" },
    { name: "Pratomagno", height: 1592, place: "Parco Foreste Casentinesi" },
    { name: "Monte Amiata", height: 1738, place: "Siena" }
  ];
   */