

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
     // parse as::  process tstamp usage


}


// example real time char js
// https://gist.github.com/skhisma/5689383



window.chartOptions = {
    segmentShowStroke: false,
    percentageInnerCutout: 75,
    animation: false
};

var chartUpdate = function(value) {
    console.log("Updating Chart: ", value);

    // Replace the chart canvas element
    $('#chart').replaceWith('<canvas id="chart" width="300" height="300"></canvas>');

    // Draw the chart
    var ctx = $('#chart').get(0).getContext("2d");
    new Chart(ctx).Doughnut([
            { value: value,
                color: '#4FD134' },
            { value: 100-value,
                color: '#DDDDDD' }],
        window.chartOptions);

    // Schedule next chart update tick
    setTimeout (function() {
        chartUpdate(value - 1);
    }, 1000); // self recursive xD / what happens if it gets under -100???
}
$(document).ready(function() {
    setTimeout (function() {
        chartUpdate(99);
    }, 1000); // 1000ms delay from starting
})


