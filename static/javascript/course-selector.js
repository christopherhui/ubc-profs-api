var subjects = ['AANB', 'ACAM', 'ADED', 'ADHE', 'AFST', 'AGEC', 'AGRO', 'AGSC', 'ANAE', 'ANAT', 'ANSC', 'ANTH', 'APBI', 'APPP', 'APSC', 'ARBC', 'ARCH', 'ARCL', 'ARST', 'ARTE', 'ARTH', 'ARTS', 'ASIA', 'ASIC', 'ASTR', 'ASTU', 'ATSC', 'AUDI', 'BA', 'BAAC', 'BABS', 'BAEN', 'BAFI', 'BAHC', 'BAHR', 'BAIM', 'BAIT', 'BALA', 'BAMA', 'BAMS', 'BAPA', 'BASC', 'BASD', 'BASM', 'BATL', 'BATM', 'BAUL', 'BIOC', 'BIOE', 'BIOF', 'BIOL', 'BMEG', 'BOTA', 'BRDG', 'BUED', 'BUSI', 'CAPS', 'CCFI', 'CCST', 'CDSC', 'CDST', 'CEEN', 'CELL', 'CENS', 'CHBE', 'CHEM', 'CHIL', 'CHIN', 'CHML', 'CICS', 'CIVL', 'CLCH', 'CLST', 'CNPS', 'CNRS', 'CNTO', 'COEC', 'COGS', 'COHR', 'COML', 'COMM', 'COMR', 'CONS', 'CPEN', 'CPSC', 'CRWR', 'CSED', 'CSIS', 'CSPW', 'CUST', 'DANI', 'DENT', 'DERM', 'DHYG', 'DMED', 'DPAS', 'DRAM', 'DSCI', 'EADM', 'ECED', 'ECON', 'EDCI', 'EDCP', 'EDST', 'EDUC', 'EECE', 'ELEC', 'EMBA', 'EMER', 'ENDS', 'ENED', 'ENGL', 'ENPH', 'ENVR', 'EOSC', 'EPSE', 'ERTH', 'ETEC', 'EXCH', 'FACT', 'FDNS', 'FEBC', 'FHIS', 'FILM', 'FINA', 'FIPR', 'FISH', 'FIST', 'FMED', 'FMPR', 'FMSC', 'FMST', 'FNEL', 'FNH', 'FNIS', 'FNLG', 'FNSP', 'FOOD', 'FOPR', 'FPEN', 'FRE', 'FREN', 'FRSI', 'FRST', 'GBPR', 'GEM', 'GENE', 'GEOB', 'GEOG', 'GEOL', 'GEOP', 'GEPA', 'GERM', 'GPP', 'GREK', 'GRS', 'GRSJ', 'GSAT', 'HCEC', 'HCEP', 'HCET', 'HEBR', 'HECO', 'HESO', 'HGSE', 'HIED', 'HIND', 'HINU', 'HIST', 'HKIN', 'HMEC', 'HMED', 'HPB', 'HUNU', 'HXAH', 'HXDR', 'HXEC', 'HXEN', 'HXFL', 'HXFR', 'HXGM', 'HXGY', 'HXHI', 'HXMA', 'HXMU', 'HXPC', 'HXPH', 'HXPS', 'HXPY', 'HXRE', 'HXSP', 'HXWR', 'IAR', 'IEST', 'IGEN', 'IHHS', 'INDE', 'INDO', 'INDS', 'INFO', 'INLB', 'ISCI', 'ITAL', 'ITST', 'IWME', 'JAPN', 'JRNL', 'KIN', 'KORN', 'LAIS', 'LANE', 'LARC', 'LASO', 'LAST', 'LATN', 'LAW', 'LFS', 'LIBE', 'LIBR', 'LING', 'LLED', 'LWS', 'MAED', 'MATH', 'MDVL', 'MECH', 'MEDD', 'MEDG', 'MEDH', 'MEDI', 'MGMT', 'MICB', 'MIDW', 'MINE', 'MLED', 'MMAT', 'MMPE', 'MRNE', 'MTRL', 'MUED', 'MUSC', 'NAME', 'NEST', 'NRSC', 'NURS', 'OBMS', 'OBST', 'OCCH', 'OCGY', 'OHS', 'OMSS', 'ONCO', 'OPTH', 'ORBI', 'ORNT', 'ORPA', 'OSOT', 'PAED', 'PATH', 'PCTH', 'PERS', 'PETE', 'PHAR', 'PHIL', 'PHRM', 'PHTH', 'PHYL', 'PHYS', 'PLAN', 'PLNT', 'POLI', 'POLS', 'PORT', 'PPEN', 'PRIN', 'PSYC', 'PSYT', 'PUNJ', 'RADI', 'READ', 'RELG', 'RES', 'RGLA', 'RGLT', 'RHSC', 'RMES', 'RMST', 'RSOT', 'RSPT', 'RUSS', 'SANS', 'SCAN', 'SCED', 'SCIE', 'SEAL', 'SLAV', 'SOAL', 'SOCI', 'SOIL', 'SOWK', 'SPAN', 'SPHA', 'SPPH', 'SSED', 'STAT', 'STS', 'SURG', 'SWED', 'SWFS', 'THTR', 'TIBT', 'TSED', 'UDES', 'UFOR', 'URDU', 'URO', 'URST', 'URSY', 'VANT', 'VISA', 'VRHC', 'WMST', 'WOOD', 'WRDS', 'WRIT', 'ZOOL']
var ctx = document.getElementById('profCompare');

var myChartCompartor = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Average',
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

const $subject = $('.subject-picker');
const $course = $('.course-picker');
const $instructor = $('.instructor-picker');

for (const subject of subjects) {
    $subject.append(`<option>${subject}</option>`);
}

$subject.on('changed.bs.select', function clickedSubject(e, clickedIndex, isSelected, previousValue) {
    const selected = $('.subject-picker option:selected').val();

    const submit = $.ajax({
        type: 'GET',
        url: `/api/subjects/courses/${selected}`
    });

    submit.done(function foundCourses(res) {
        $course.empty();
        $instructor.empty();
        for (const course of res) {
            $course.append(`<option>${course}</option>`)
        }
        $course.selectpicker('refresh');
        $instructor.selectpicker('refresh');
    });

    submit.fail(function failed(e) {
        console.log(e, '¯\\_(ツ)_/¯');
    })
});

$course.on('changed.bs.select', function clickedSubject(e, clickedIndex, isSelected, previousValue) {
    const selected0 = $('.subject-picker option:selected').val();
    const selected1 = $('.course-picker option:selected').val();

    const submit = $.ajax({
        type: 'GET',
        url: `/api/professors/${selected0}/${selected1}`
    });

    submit.done(function foundInstructors(res) {
        $instructor.empty();
        for (const instructor of res) {
            $instructor.append(`<option>${instructor}</option>`)
        }
        $instructor.selectpicker('refresh');
    });

    submit.fail(function failed(e) {
        console.log(e, '¯\\_(ツ)_/¯');
    })
});

function compare() {
    const subject = $('.subject-picker option:selected').val();
    const course = $('.course-picker option:selected').val();

    let instructorsSelected = [];
    $.each($(".instructor-picker option:selected"), function () {
        instructorsSelected.push($(this).val());
    });

    let maxAvg = 0;
    let avgInst = '';
    let lowStdev = 0;
    let stdevInst = '';
    let maxYears = 0;
    let yearsInst = '';
    let maxStud = 0;
    let studInst = '';

    myChartCompartor.data.labels = instructorsSelected;

    for (let instructor of instructorsSelected) {
        const submit = $.ajax({
            type: 'GET',
            url: `/api/general-stats-verbose/${instructor}/${subject}/${course}`
        });

        submit.done({

        });

        submit.fail(function (err) {
            console.log(err, "What's the error again?");
        })
    }
}
