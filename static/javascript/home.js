var ctx = document.getElementById('generalStats');
var xmlhttp = new XMLHttpRequest();

var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
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

document.getElementById("search-input-prof").onkeyup = function findResults() {
    const profInput = document.getElementById("search-input-prof").value;
    const theUrl = "/api/professors";
    $('#result').empty();

    if (profInput.length >= 2) {
        xmlhttp.open("POST", theUrl);
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify({"prof": document.getElementById("search-input-prof").value}));

        xmlhttp.onreadystatechange = function () {
            profsResult = xmlhttp.responseText ? JSON.parse(xmlhttp.responseText) : [];
            let counter = 0;

            for (prof of profsResult) {
                if (counter === 5) {
                    break;
                }
                $('#result').append('<li class="list-group-item link-class">' + prof);
                counter++;
            }
            // return xmlhttp.responseText;
        };
    }
};

$('#result').on('click', 'li', function () {
    var click_text = $(this).text().split('|');
    $('#search-input-prof').val($.trim(click_text[0]));
    $("#result").html('');
});