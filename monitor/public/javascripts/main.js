console.log("main.js");

$(document).ready(function () {

    $.ajax({
        type: "GET",
        url: "/data/Memory_append.log",
        dataType: "text",
        success: function (data) {
            processData(data);
        }
    });
});

function processData(allText) {
    var lines = allText.split('\n')
    var matrix = lines.map(function (line) {
        return line.split(' ')
    })
    console.log(matrix)
}

function renderLastValue(logfile, delay) {
    $.ajax({
        type: "GET",
        url: "/data/" + logfile,
        dataType: "text",
        success: function (data) {
            var type = ''
            var t = logfile.split('_')[0]
            console.log(t)
            switch (t) {
                case 'Memory':
                    type = 'ram';
                    break;
                case 'Process':
                    type = 'cpu';
                    break;
                case 'Disk':
                    type = 'hdd';
                    break;
                default :
                    break;
            }
            processDataLatest(data, type);
            setTimeout(function () {
                renderLastValue(logfile, delay)
            }, delay)
        }
    });
}

function processDataLatest(allText, type) {
    // console.log(allText)
    var lines = allText.split('\n')
    // console.log(lines)
    var last = lines[lines.length - 1].split(' ')
    if (last == '') {
        var rdm = Math.floor(Math.random() * (lines.length))
        last = lines[rdm].split(' ')
    }
    console.log(last, type)
    renderGraph(parseFloat(last[2]), type)
}

// example real time char js
// https://gist.github.com/skhisma/5689383


window.chartOptions = {
    segmentShowStroke: false,
    percentageInnerCutout: 75,
    animation: false
};


$(document).ready(function () {
    setTimeout(function () {
        renderLastValue('Memory_append.log', 1000) // starting with 0 # this can infer with the real results average, but this is just for monitor
        renderLastValue('Process_append.log', 1000)
        renderLastValue('Disk_append.log', 1000)
    }, 1000); // 1000ms delay from starting
})


function renderGraph(value, type) {

    console.log("Updating Chart: ", value);
    var canvasname = "chart_"+type;
    // Replace the chart canvas element
    $('#'+canvasname).replaceWith("<canvas id=\""+canvasname+"\" width=\"100\" height=\"100\"></canvas>"); // at each refreash clean...

    var ctx = $('#'+canvasname).get(0).getContext("2d");
    new Chart(ctx)
        .Doughnut([{value: value, color: '#4FD134'}, {value: 100 - value, color: '#DDDDDD'}], window.chartOptions);

}

