

console.log("main.js");

$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "/data/Memory_append.log",
        dataType: "text",
        success: function(data) {processData(data);}
    });
});

function processData(allText) {
     console.log(allText)
     // plot this stuff
     // parse as process tstamp cpu usage
}


