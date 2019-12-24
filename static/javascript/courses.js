// TODO: Once they type something, clear form from subject, course, year

function formatProfName(profName) {
    profName = profName.replace(/, /g, '-');
    profName = profName.replace(/ /g, '-');
    return profName;
}

function profSearchCustom() {
    let profInput = $('#search-input-prof').val();
    profInput = formatProfName(profInput);
    const subject = $('#dropdownMenuButtonSubject');
    const course = $('#dropdownMenuButtonCourse');
    const year = $('#dropdownMenuButtonYear');
    const section = $('#dropdownMenuButtonSection');

    if (subject.text() === "All") {
        search(`/api/general-stats/${profInput}`);
    } else if (course.text() === "All") {
        search(`/api/general-stats/${profInput}/${subject.text()}`)
    } else if (year.text() === "All") {
        search(`/api/general-stats/${profInput}/${subject.text()}/${course.text()}`)
    } else if (section.text() === "All") {
        search(`/api/general-stats/${profInput}/${subject.text()}/${course.text()}/${year.text()}`)
    } else {
        search(`/api/general-stats/${profInput}/${subject.text()}/${course.text()}/${year.text()}/${section.text()}`)
    }
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
        const course_dropdown = $('#course-dropdown');
        course_dropdown.empty();
        course_dropdown.append('<a class="dropdown-item" href="javascript:void(0)">All</a>');
        for (let course of res) {
            course_dropdown.append('<a class="dropdown-item" href="javascript:void(0)">' + course + '</a>')
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
        const year_dropdown = $('#year-dropdown');
        year_dropdown.empty();
        year_dropdown.append('<a class="dropdown-item" href="javascript:void(0)">All</a>');
        for (let year of res) {
            year_dropdown.append('<a class="dropdown-item" href="javascript:void(0)">' + year + '</a>')
        }
    });

    submit.fail(function failed(msg) {
        console.log(msg, "F");
    })
});

$('#year-dropdown').on('click', 'a', function clickOnSubjectResult() {
    let prof = $('#search-input-prof').val();
    prof = formatProfName(prof);
    const subject = $('#dropdownMenuButtonSubject').text();
    const course = $('#dropdownMenuButtonCourse').text();

    const click_text = $(this).text().split('|');
    $('#dropdownMenuButtonYear').text(click_text[0]);

    const submit = $.ajax({
        type: "GET",
        url: `/api/sections/${prof}/${subject}/${course}/${click_text[0]}`
    });

    submit.done(function getAllSections(res) {
        const section_dropdown = $('#section-dropdown');
        section_dropdown.empty();
        section_dropdown.append('<a class="dropdown-item" href="javascript:void(0)">All</a>');
        for (let section of res) {
            section_dropdown.append('<a class="dropdown-item" href="javascript:void(0)">' + section + '</a>')
        }
    });

    submit.fail(function failed(msg) {
        console.log(msg, "F");
    })
});

$('#section-dropdown').on('click', 'a', function clickOnSubjectResult() {
    const click_text = $(this).text().split('|');
    $('#dropdownMenuButtonSection').text(click_text[0]);
});
