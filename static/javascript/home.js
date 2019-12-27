var ctx = document.getElementById('generalStats');
var stats = null;
var done = false;
var fuse = null;

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

function reverse(prof) {
    prof = formatProfName(prof);
    prof = prof.split('-').reverse().join(' ');
    return prof;
}

document.getElementById("search-input-prof").onkeydown = function findResults() {
    const profInput = document.getElementById("search-input-prof").value;
    $('#result').empty();
    $('.search-status').empty();

    if (profInput.length >= 2 && !done) {
        done = true;
        let submit = $.ajax({
            type: 'GET',
            url: '/api/professors'
        });

        submit.done(function gotProfs(profs) {

            var searchProfs = profs.map(prof => ({'name': prof, 'name_cut': formatProfName(prof).split('-').join(' '), 'name_backwards': reverse(prof)}));
            var options = {
                shouldSort: true,
                keys: [{name: 'name_cut', weight: 0.3}, {name: 'name_backwards', weight: 0.7}],
                id: 'name'
            };
            fuse = new Fuse(searchProfs, options);
            const profsResult = fuse.search(profInput).slice(0, 5);

            for (let prof of profsResult) {
                $('#result').append('<li class="list-group-item link-class" id="prof-name">' + prof);
            }
        });

        submit.fail(function noProfs(err) {
            console.log('No profs found');
        });
    } else if (profInput.length >= 2) {
        const profsResult = fuse.search(profInput).slice(0, 5);

        for (let prof of profsResult) {
            $('#result').append('<li class="list-group-item link-class" id="prof-name">' + prof);
        }
    }
};


$('#result').on('click', 'li', function clickOnProfResult() {
    var click_text = $(this).text().split('|');
    $('#search-input-prof').val($.trim(click_text[0]));
    $("#result").html('');
    $('#dropdownMenuButtonSubject').text('All');

    clearCourse();
    clearYear();
    clearSection();

    let profInput = click_text[0];
    profInput = formatProfName(profInput);

    const submit = $.ajax({
        type: "GET",
        url: `/api/courses/${profInput}`
    });

    submit.done(function getAllSubjects(res) {
        const subject_dropdown = $('#subject-dropdown');
        subject_dropdown.empty();
        subject_dropdown.append('<a class="dropdown-item" href="javascript:void(0)">All</a>');
        for (let subject of res) {
            subject_dropdown.append('<a class="dropdown-item subject-item" href="javascript:void(0)">' + subject + '</a>')
        }
    });

    submit.fail(function failed(msg) {
        console.log(msg, "Bruh... What did you do?")
    })
});

function profSearch() {
    let profInput = $('#search-input-prof').val();
    profInput = formatProfName(profInput);
    const theUrl = `/api/general-stats-verbose/${profInput}`;
    search(theUrl);
}

// Todo: #overall-* is used in many html files, and this function can be used many times, any refactoring required?
function search(theUrl) {
    const search1 = $(".search-status");
    search1.empty();

    const submit = $.ajax({
        type: "GET",
        url: theUrl
    });

    submit.done(function gotResults(res) {
        const search1 = $(".search-status");
        if (res['stats']['name'] === '') {
            search1.append("<span class=\"input-group-text bg-warning text-white\" id=\"inputGroup-sizing-default\">No information was found.</span>");
        } else {
            stats = res;
            changeToUndergrad();
            search1.append("<span class=\"input-group-text bg-success text-white\" id=\"inputGroup-sizing-default\">Success!</span>");
        }
    });

    submit.fail(function noResult(err) {
        search1.append("<span class=\"input-group-text bg-warning text-white\" id=\"inputGroup-sizing-default\">No information was found.</span>");
    });
}

function changeToUndergrad() {
    const underGradRes = stats["undergrad"];
    const underGradGrades = underGradRes["grades"];
    const underGradStats = stats["stats"]["undergrad"];
    const data = [underGradGrades["0-9%"], underGradGrades["10-19%"], underGradGrades["20-29%"], underGradGrades["30-39%"],
        underGradGrades["40-49%"], underGradGrades["50-54%"], underGradGrades["55-59%"], underGradGrades["60-63%"],
        underGradGrades["64-67%"], underGradGrades["68-71%"], underGradGrades["72-75%"], underGradGrades["76-79%"],
        underGradGrades["80-84%"], underGradGrades["85-89%"], underGradGrades["90-100%"]];

    addProfData(myChart, data);
    $("#overall-avg").text(underGradRes["average"].toFixed(2));
    $("#overall-std").text(underGradRes["stdev"].toFixed(2));
    $("#overall-median").text(underGradRes["median"].toFixed(2));
    $("#overall-passed").text(underGradRes["pass"].toFixed(2));
    $("#home-graph").text("Undergraduate Grade Distribution");

    $("#prof-name").text(stats["stats"]["name"]);
    $("#students-taught").text(underGradStats["count"]);
    $("#subjects-taught").text(underGradStats["subjects_taught"].join(", "));
    $("#highest-course-average").text(`${underGradStats["avg_high"]}, (${underGradStats["subject_high"]}${underGradStats["course_high"]}, ${underGradStats["year_high"]})`);
    $("#lowest-course-average").text(`${underGradStats["avg_low"]}, (${underGradStats["subject_low"]}${underGradStats["course_low"]}, ${underGradStats["year_low"]})`);
}

function changeToAll() {
    const allRes = stats["all"];
    const allGrades = allRes["grades"];
    const allStats = stats["stats"]["all"];
    const data = [allGrades["0-9%"], allGrades["10-19%"], allGrades["20-29%"], allGrades["30-39%"],
        allGrades["40-49%"], allGrades["50-54%"], allGrades["55-59%"], allGrades["60-63%"],
        allGrades["64-67%"], allGrades["68-71%"], allGrades["72-75%"], allGrades["76-79%"],
        allGrades["80-84%"], allGrades["85-89%"], allGrades["90-100%"]];
    addProfData(myChart, data);
    $("#overall-avg").text(allRes["average"].toFixed(2));
    $("#overall-std").text(allRes["stdev"].toFixed(2));
    $("#overall-median").text(allRes["median"].toFixed(2));
    $("#overall-passed").text(allRes["pass"].toFixed(2));
    $("#home-graph").text("Overall Grade Distribution");

    $("#prof-name").text(stats["stats"]["name"]);
    $("#students-taught").text(allStats["count"]);
    $("#subjects-taught").text(allStats["subjects_taught"].join(", "));
    $("#highest-course-average").text(`${allStats["avg_high"]}, (${allStats["subject_high"]}${allStats["course_high"]}, ${allStats["year_high"]})`);
    $("#lowest-course-average").text(`${allStats["avg_low"]}, (${allStats["subject_low"]}${allStats["course_low"]}, ${allStats["year_low"]})`);
}