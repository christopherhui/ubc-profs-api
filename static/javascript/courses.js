// TODO: Once they type something, clear form from subject, course, year

function formatProfName(profName) {
    profName = profName.replace(/, /g, '-');
    profName = profName.replace(/ /g, '-');
    return profName;
}

$('#subject-dropdown').on('click', 'a', function clickOnSubjectResult() {
    let prof = $('#search-input-prof').val();
    prof = formatProfName(prof);

    const click_text = $(this).text().split('|');
    $('#dropdownMenuButtonSubject').text(click_text[0]);

    const submit = $.ajax({
        type: "GET",
        url: `/api/subjects/${prof}/${click_text[0]}`
    });

    submit.done(function getAllYears(res) {
        $('#course-dropdown').empty();
        for (let course of res) {
            $('#course-dropdown').append('<a class="dropdown-item" href="javascript:void(0)">' + course + '</a>')
        }
    });

    submit.fail(function failed(msg) {
        console.log(msg, "F");
    })
});

$('#course-dropdown').on('click', 'a', function clickOnSubjectResult() {
    let prof = $('#search-input-prof').val();
    prof = formatProfName(prof);
    const subject = $('#dropdownMenuButtonSubject').text();

    const click_text = $(this).text().split('|');
    $('#dropdownMenuButtonCourse').text(click_text[0]);

    const submit = $.ajax({
        type: "GET",
        url: `/api/years/${prof}/${subject}/${click_text[0]}`
    });

    submit.done(function getAllYears(res) {
        $('#year-dropdown').empty();
        for (let year of res) {
            $('#year-dropdown').append('<a class="dropdown-item" href="javascript:void(0)">' + year + '</a>')
        }
    });

    submit.fail(function failed(msg) {
        console.log(msg, "F");
    })
});

