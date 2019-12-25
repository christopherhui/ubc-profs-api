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

function profSearchTime() {
    let profInput = $('#search-input-prof').val();
    profInput = formatProfName(profInput);

    const submit = $.ajax({
        type: 'GET',
        url: `/api/stats/years/${profInput}`
    });

    submit.done(function getYears(res) {
        myLineChart.data.labels = Object.keys(res);
        const stuff = Object.values(res);
        myLineChart.data.datasets[0].data = stuff.map(x => x['average']);
        myLineChart.data.datasets[1].data = stuff.map(x => x['high']);
        myLineChart.data.datasets[2].data = stuff.map(x => x['low']);
        myLineChart.update();
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