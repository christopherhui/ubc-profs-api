var ctx = document.getElementById('avg-date');

var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Average grade overtime',
                data: [],
                backgroundColor: ['rgba(255, 99, 132, 0.2)']
            },
            {
                label: 'Max grade overtime',
                data: [],
                backgroundColor: ['rgba(54, 162, 235, 0.2)']
            },
            {
                label: 'Min grade overtime',
                data: [],
                backgroundColor: ['rgba(75, 192, 192, 0.2)']
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});

function formatProfName(profName) {
    profName = profName.replace(/, /g, '-');
    profName = profName.replace(/ /g, '-');
    return profName;
}

function profSearchTime() {
    let profInput = $('#search-input-prof').val();
    profInput = formatProfName(profInput);

    const submit = $.ajax({
        type: 'GET',
        url: `/api/stats/years/${profInput}`
    });

    submit.done(function getYears(res) {
        const years = Object.keys(res);
        const stuff = Object.values(res);
        const averages = stuff.map(x => x['average'].toFixed(2));
        const highs = stuff.map(x => x['high'].toFixed(0));
        const lows = stuff.map(x => x['low'].toFixed(0));

        myLineChart.data.labels = years;
        myLineChart.data.datasets[0].data = averages;
        myLineChart.data.datasets[1].data = highs;
        myLineChart.data.datasets[2].data = lows;
        myLineChart.update();

        const columns = $('#columns-date');
        columns.empty();
        columns.append("<th scope=\"col\">Data</th>");
        const $average = $('#average-date');
        $average.empty();
        $average.append('<th scope="row">Average</th>');
        const $max = $('#max-date');
        $max.empty();
        $max.append('<th scope="row">Max Grade</th>');
        const $min = $('#min-date');
        $min.empty();
        $min.append('<th scope="row">Min Grade</th>');

        years.forEach(year => columns.append(`<th scope="col">${year}</th>`));
        averages.forEach(average => $average.append(`<td>${average}</td>`));
        highs.forEach(high => $max.append(`<td>${high}</td>`));
        lows.forEach(low => $min.append(`<td>${low}</td>`));
    });

    submit.fail(function noResult(err) {
        console.log(err, "Aw man!");
    })
}

document.getElementById("search-input-prof").onkeydown = function findResults() {
    const xhr = new XMLHttpRequest();
    const profInput = document.getElementById("search-input-prof").value;
    const theUrl = "/api/professors";
    $('#result').empty();
    $('.search-status').empty();

    if (profInput.length >= 2) {
        xhr.onload = function () {
            const profsResult = xhr.responseText ? JSON.parse(xhr.responseText) : [];

            for (let prof of profsResult) {
                $('#result').append('<li class="list-group-item link-class" id="prof-name">' + prof);
            }
        };

        xhr.open("POST", theUrl);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({"prof": document.getElementById("search-input-prof").value}));
    }
};

$('#result').on('click', 'li', function clickOnProfResult() {
    var click_text = $(this).text().split('|');
    $('#search-input-prof').val($.trim(click_text[0]));
    $("#result").html('');
    $('#dropdownMenuButtonSubject').text('All');
});