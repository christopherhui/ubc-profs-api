var ctx = document.getElementById('generalStats');

var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['0-9%', '10-19%', '20-29%', '30-39%', '40-49%', '50-54%', '55-59%', '60-63%', '64-67%', '68-71%',
            '72-75%', '76-79%', '80-84%', '85-89%', '90-100%'],
        datasets: [{
            label: 'General Statistics Distribution',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)'
            ],
            borderWidth: 1
        }]
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

function addProfData(chart, data) {
    chart.data.datasets[0].data = data;
    chart.update();
}

document.getElementById("search-input-prof").onkeydown = function findResults() {
    const xhr = new XMLHttpRequest();
    const profInput = document.getElementById("search-input-prof").value;
    const theUrl = "/api/professors";
    $('#result').empty();

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

    let profInput = click_text[0];
    profInput = formatProfName(profInput);

    const submit = $.ajax({
        type: "GET",
        url: `/api/courses/${profInput}`
    });

    submit.done(function getAllSubjects(res) {
        $('#subject-dropdown').empty();
        for (let subject of res) {
            $('#subject-dropdown').append('<a class="dropdown-item subject-item" href="javascript:void(0)">' + subject + '</a>')
        }
    });

    submit.fail(function failed(msg) {
        console.log(msg, "Bruh... What did you do?")
    })
});

function profSearch() {
    let profInput = document.getElementById("search-input-prof").value;
    profInput = formatProfName(profInput);
    const theUrl = `/api/general-stats/${profInput}`;

    const submit = $.ajax({
        type: "GET",
        url: theUrl
    });

    submit.done(function gotResults(res) {
        // Undergraduate results for now
        const underGradRes = res["undergrad"];
        const underGradGrades = underGradRes["grades"];
        const data = [underGradGrades["0-9%"], underGradGrades["10-19%"], underGradGrades["20-29%"], underGradGrades["30-39%"],
            underGradGrades["40-49%"], underGradGrades["50-54%"], underGradGrades["55-59%"], underGradGrades["60-63%"],
            underGradGrades["64-67%"], underGradGrades["68-71%"], underGradGrades["72-75%"], underGradGrades["76-79%"],
            underGradGrades["80-84%"], underGradGrades["85-89%"], underGradGrades["90-100%"]];
        addProfData(myChart, data);
        $("#overall-avg").text(underGradRes["average"].toFixed(2));
        $("#overall-std").text(underGradRes["stdev"].toFixed(2));
        $("#overall-median").text(underGradRes["median"].toFixed(2));
        $("#overall-passed").text(underGradRes["pass"].toFixed(2));
    });

    submit.fail(function noResult(err) {
        console.log(err, "Certified Bruh Moment");
    });
}