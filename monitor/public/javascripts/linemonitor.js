$('document').ready(function () {

    console.log("Ready");


    var smoothie = new SmoothieChart(
        {
            grid: {
                strokeStyle: 'rgb(125, 0, 0)',
                fillStyle: 'rgb(60, 0, 0)',
                lineWidth: 1,
                millisPerLine: 250,
                verticalSections: 6
            },
            labels: {
                fillStyle: 'rgb(60, 0, 0)'
            },
            minValue: 0,
            maxValue: 100
        }
    );
    var streamDelay = 1000;
    smoothie.streamTo(document.getElementById("mycanvas"), streamDelay);
// Data
    var lineCpu = new TimeSeries();
    // var line2 = new TimeSeries();


// Add to SmoothieChart

    smoothie.addTimeSeries(lineCpu, {
            strokeStyle: 'rgb(0, 255, 0)',
            fillStyle: 'rgba(0, 255, 0, 0.4)',
            lineWidth: 3
        }
    );
    // smoothie.addTimeSeries(line2);

// Add a random value to each line every second

    var interval = 1000; // chart udate interval

    renderLastValue('Process_append.log', interval, function (data, type) {
        var lines = data.split('\n')
        var last = lines[lines.length - 2] // no mostrar ultimo siempre el penultimo porque el ultimo es un ""
        last = last.split(' ')
        var usage = parseFloat(last[2]);
        console.log(last, type)
        console.log('Callback: ' + usage)
        lineCpu.append(new Date().getTime(), usage);
    });


    console.log("Smoothie")


});


function renderLastValue(logfile, delay, cb) {
    $.ajax({
        type: "GET",
        url: "/data/" + logfile,
        dataType: "text",
        success: function (data) {
            var type = '';
            var t = logfile.split('_')[0];
            console.log(t);
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

            cb(data, type);

            // calling self again

            setTimeout(function () {
                renderLastValue(logfile, delay, cb)
            }, delay)

        }
    });
}






