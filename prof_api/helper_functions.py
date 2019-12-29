import math
import sqlite3
import re
import statistics
from collections import OrderedDict

from flask import jsonify

stats_cat = ['average', 'stdev', 'high', 'low', 'passed', 'fail', 'withdrew', 'audit', 'other']
grades_cat = {'g0to9': '0-9%', 'g10to19': '10-19%', 'g20to29': '20-29%', 'g30to39': '30-39%', 'g40to49': '40-49%','gless50': '<50%', 'g50to54': '50-54%', 'g55to59': '55-59%', 'g60to63': '60-63%', 'g64to67': '64-67%','g68to71': '68-71%', 'g72to75': '72-75%', 'g76to79': '76-79%', 'g80to84': '80-84%', 'g85to89': '85-89%','g90to100': '90-100%'}
yearsessions = ['1996S', '1996W', '1997S', '1997W', '1998S', '1998W', '1999S', '1999W', '2000S', '2000W', '2001S','2001W', '2002S', '2002W', '2003S', '2003W', '2004S', '2004W', '2005S', '2005W', '2006S', '2006W','2007S', '2007W', '2008S', '2008W', '2009S', '2009W', '2010S', '2010W', '2011S', '2011W', '2012S','2012W', '2013S', '2013W', '2014S', '2014W', '2015S', '2015W', '2016S', '2016W', '2017S', '2017W','2018S', '2018W']
subjects = ['AANB', 'ACAM', 'ADED', 'ADHE', 'AFST', 'AGEC', 'AGRO', 'AGSC', 'ANAE', 'ANAT', 'ANSC', 'ANTH', 'APBI','APPP', 'APSC', 'ARBC', 'ARCH', 'ARCL', 'ARST', 'ARTE', 'ARTH', 'ARTS', 'ASIA', 'ASIC', 'ASTR', 'ASTU','ATSC', 'AUDI', 'BA', 'BAAC', 'BABS', 'BAEN', 'BAFI', 'BAHC', 'BAHR', 'BAIM', 'BAIT', 'BALA', 'BAMA','BAMS', 'BAPA', 'BASC', 'BASD', 'BASM', 'BATL', 'BATM', 'BAUL', 'BIOC', 'BIOE', 'BIOF', 'BIOL', 'BMEG','BOTA', 'BRDG', 'BUED', 'BUSI', 'CAPS', 'CCFI', 'CCST', 'CDSC', 'CDST', 'CEEN', 'CELL', 'CENS', 'CHBE','CHEM', 'CHIL', 'CHIN', 'CHML', 'CICS', 'CIVL', 'CLCH', 'CLST', 'CNPS', 'CNRS', 'CNTO', 'COEC', 'COGS','COHR', 'COML', 'COMM', 'COMR', 'CONS', 'CPEN', 'CPSC', 'CRWR', 'CSED', 'CSIS', 'CSPW', 'CUST', 'DANI','DENT', 'DERM', 'DHYG', 'DMED', 'DPAS', 'DRAM', 'DSCI', 'EADM', 'ECED', 'ECON', 'EDCI', 'EDCP', 'EDST','EDUC', 'EECE', 'ELEC', 'EMBA', 'EMER', 'ENDS', 'ENED', 'ENGL', 'ENPH', 'ENVR', 'EOSC', 'EPSE', 'ERTH','ETEC', 'EXCH', 'FACT', 'FDNS', 'FEBC', 'FHIS', 'FILM', 'FINA', 'FIPR', 'FISH', 'FIST', 'FMED', 'FMPR','FMSC', 'FMST', 'FNEL', 'FNH', 'FNIS', 'FNLG', 'FNSP', 'FOOD', 'FOPR', 'FPEN', 'FRE', 'FREN', 'FRSI','FRST', 'GBPR', 'GEM', 'GENE', 'GEOB', 'GEOG', 'GEOL', 'GEOP', 'GEPA', 'GERM', 'GPP', 'GREK', 'GRS', 'GRSJ','GSAT', 'HCEC', 'HCEP', 'HCET', 'HEBR', 'HECO', 'HESO', 'HGSE', 'HIED', 'HIND', 'HINU', 'HIST', 'HKIN','HMEC', 'HMED', 'HPB', 'HUNU', 'HXAH', 'HXDR', 'HXEC', 'HXEN', 'HXFL', 'HXFR', 'HXGM', 'HXGY', 'HXHI','HXMA', 'HXMU', 'HXPC', 'HXPH', 'HXPS', 'HXPY', 'HXRE', 'HXSP', 'HXWR', 'IAR', 'IEST', 'IGEN', 'IHHS','INDE', 'INDO', 'INDS', 'INFO', 'INLB', 'ISCI', 'ITAL', 'ITST', 'IWME', 'JAPN', 'JRNL', 'KIN', 'KORN','LAIS', 'LANE', 'LARC', 'LASO', 'LAST', 'LATN', 'LAW', 'LFS', 'LIBE', 'LIBR', 'LING', 'LLED', 'LWS', 'MAED','MATH', 'MDVL', 'MECH', 'MEDD', 'MEDG', 'MEDH', 'MEDI', 'MGMT', 'MICB', 'MIDW', 'MINE', 'MLED', 'MMAT','MMPE', 'MRNE', 'MTRL', 'MUED', 'MUSC', 'NAME', 'NEST', 'NRSC', 'NURS', 'OBMS', 'OBST', 'OCCH', 'OCGY','OHS', 'OMSS', 'ONCO', 'OPTH', 'ORBI', 'ORNT', 'ORPA', 'OSOT', 'PAED', 'PATH', 'PCTH', 'PERS', 'PETE','PHAR', 'PHIL', 'PHRM', 'PHTH', 'PHYL', 'PHYS', 'PLAN', 'PLNT', 'POLI', 'POLS', 'PORT', 'PPEN', 'PRIN','PSYC', 'PSYT', 'PUNJ', 'RADI', 'READ', 'RELG', 'RES', 'RGLA', 'RGLT', 'RHSC', 'RMES', 'RMST', 'RSOT','RSPT', 'RUSS', 'SANS', 'SCAN', 'SCED', 'SCIE', 'SEAL', 'SLAV', 'SOAL', 'SOCI', 'SOIL', 'SOWK', 'SPAN','SPHA', 'SPPH', 'SSED', 'STAT', 'STS', 'SURG', 'SWED', 'SWFS', 'THTR', 'TIBT', 'TSED', 'UDES', 'UFOR','URDU', 'URO', 'URST', 'URSY', 'VANT', 'VISA', 'VRHC', 'WMST', 'WOOD', 'WRDS', 'WRIT', 'ZOOL']


def find_name(professor):
    """
    Takes a name from webpage and makes it possible to query in the database

    :param professor: name of professor in dash form
    :return: name of professor used for querying database and '' if not found
    """
    from api import app
    name = professor.split('-')
    query = 'SELECT name FROM professor WHERE name LIKE ?;'

    conn = sqlite3.connect(app.config['DATABASE_NAME'])
    cur = conn.cursor()
    all_prof_names = cur.execute(query, ['%{}%'.format(name[0])]).fetchall()
    for prof_name in all_prof_names:
        cut_prof_name = re.sub('[-, ]', '', prof_name[0])
        if cut_prof_name.lower() == ''.join(name).lower():
            return prof_name[0]
    return ''


def result_to_json(cursor, row):
    """

    :return: json version of results
    """
    from api import app
    d = {}
    d['grades'] = {}
    d['stats'] = {}
    for idx, col in enumerate(cursor.description):
        if col[0] == 'id' or col[0] == 'course_id':
            continue
        elif col[0] in grades_cat:
            d['grades'][grades_cat[col[0]]] = row[idx]
        elif col[0] in stats_cat:
            if col[0] == 'passed':
                d['stats']['pass'] = row[idx]
            else:
                d['stats'][col[0]] = row[idx]
        else:
            d[col[0]] = row[idx]
    return d


def general_get(professor, add_query='', *options):
    """
    General function for querying in database for professor and returning
    JSON formatted result

    :param professor: In forms of sqlite database name (Last, First)
    :param add_query:
    :param options:
    :return:
    """
    from api import app
    query = 'SELECT course.*, stats.*, grades.* FROM professor ' \
            'INNER JOIN association ON professor.id = association.professor_id ' \
            'INNER JOIN course ON course.id = association.course_id ' \
            'INNER JOIN stats ON course.id=stats.course_id ' \
            'INNER JOIN grades ON course.id = grades.course_id ' \
            'WHERE professor.name = ? ' + add_query

    conn = sqlite3.connect(app.config['DATABASE_NAME'])
    conn.row_factory = result_to_json
    cur = conn.cursor()
    new_options = [professor] + [x for x in options if x != 'fetchone']
    if 'fetchone' in options:
        results = cur.execute(query, new_options).fetchone()
    else:
        results = cur.execute(query, new_options).fetchall()

    return jsonify(results)


def calculate_all_to_json(all_arr, all_std, d, pass_ratio_all, count):
    if len(all_arr) > 0:
        d['all']['average'] = statistics.mean(all_arr) if len(all_arr) >= 2 else all_arr[0]
        d['all']['stdev'] = math.sqrt(sum(all_std))/len(all_std) if len(all_std) >= 2 else math.sqrt(all_std[0])
        d['all']['median'] = statistics.median(all_arr) if len(all_arr) >= 2 else all_arr[0]
        d['all']['pass'] = pass_ratio_all/count


def calculate_undergrad_to_json(d, pass_ratio_undergrad, undergrad_arr, undergrad_std, count):
    if len(undergrad_arr) > 0:
        d['undergrad']['average'] = statistics.mean(undergrad_arr) if len(undergrad_arr) >= 2 else undergrad_arr[0]
        d['undergrad']['stdev'] = math.sqrt(sum(undergrad_std))/len(undergrad_std) if len(undergrad_std) >= 2 else math.sqrt(undergrad_std[0])
        d['undergrad']['median'] = statistics.median(undergrad_arr) if len(undergrad_arr) >= 2 else undergrad_arr[0]
        d['undergrad']['pass'] = pass_ratio_undergrad/count


def add_grade_values(course_no, d, grades):
    for grade_bound, grade in grades.items():
        if grade_bound not in d['all']['grades']:
            d['all']['grades'][grade_bound] = grade
        else:
            d['all']['grades'][grade_bound] += grade

        if course_no < 500:
            if grade_bound not in d['undergrad']['grades']:
                d['undergrad']['grades'][grade_bound] = grade
            else:
                d['undergrad']['grades'][grade_bound] += grade


def get_statistics(d, professor, json_query):
    values = json_query
    d['stats'] = {}
    d['stats']['name'] = find_name(professor)

    yearsU = set()
    yearsA = set()

    taughtU = set()
    taughtA = set()

    countU = 0
    countA = 0

    highavgU = 0
    highsubjectU = ''
    highcourseU = ''
    highyearU = ''

    lowavgU = 100
    lowsubjectU = ''
    lowcourseU = ''
    lowyearU = ''

    highavgA = 0
    highsubjectA = ''
    highcourseA = ''
    highyearA = ''

    lowavgA = 100
    lowsubjectA = ''
    lowcourseA = ''
    lowyearA = ''

    for val in values:
        subject = val['subject']
        course = val['course']
        year = val['year_session']
        avg = val['stats']['average']

        try:
            course_no = int(course)
        except ValueError:
            course_no = int(course[0:3])

        countA += val['enrolled']
        yearsA.add(year)
        taughtA.add(subject)

        if avg == '':
            continue

        if course_no < 500:
            if avg > highavgU:
                highavgU = avg
                highsubjectU = subject
                highcourseU = course
                highyearU = year

            if avg < lowavgU:
                lowavgU = avg
                lowsubjectU = subject
                lowcourseU = course
                lowyearU = year

            countU += val['enrolled']
            yearsU.add(year)
            taughtU.add(subject)

        if avg > highavgA:
            highavgA = avg
            highsubjectA = subject
            highcourseA = course
            highyearA = year

        if avg < lowavgA:
            lowavgA = avg
            lowsubjectA = subject
            lowcourseA = course
            lowyearA = year

    d['stats']['undergrad'] = {
        'avg_high': highavgU,
        'subject_high': highsubjectU,
        'course_high': highcourseU,
        'year_high': highyearU,
        'avg_low': lowavgU,
        'subject_low': lowsubjectU,
        'course_low': lowcourseU,
        'year_low': lowyearU,
        'count': countU,
        'years_taught': list(yearsU),
        'subjects_taught': list(taughtU)
    }
    d['stats']['all'] = {
        'avg_high': highavgA,
        'subject_high': highsubjectA,
        'course_high': highcourseA,
        'year_high': highyearA,
        'avg_low': lowavgA,
        'subject_low': lowsubjectA,
        'course_low': lowcourseA,
        'year_low': lowyearA,
        'count': countA,
        'years_taught': list(yearsA),
        'subjects_taught': list(taughtA)
    }
    return d


def convert_to_general_overall(json_query):
    """
    Given a JSON query, typically with multiple courses, returns the
    general statistics of all courses under which the JSON query contains
    :param json_query:
    :return:
    """
    if len(json_query) == 0:
        return {}

    d = {
        'undergrad': {
            'grades': {},
            'average': 0,
            'stdev': 0,
            'median': 0,
            'pass': 0
        },
        'all': {
            'grades': {},
            'average': 0,
            'stdev': 0,
            'median': 0,
            'pass': 0
        }
    }

    pass_ratio_undergrad = 0
    undergrad_arr = []
    undergrad_std = []
    count_undergrad = 0

    pass_ratio_all = 0
    all_arr = []
    all_std = []
    count_all = 0

    for query in json_query:
        grades = query['grades']
        stats = query['stats']

        # Attempts to find whether or the course has an additional letter at the end
        # If it does, then we will use the condensed version
        try:
            course_no = int(query['course'])
        except ValueError:
            course_no = int(query['course'][0:3])

        # Check that there are actually statistics for this course before adding values in
        if stats['average'] == '':
            continue

        add_grade_values(course_no, d, grades)

        if course_no < 500:
            undergrad_arr.append(stats['average'])
            undergrad_std.append(stats['stdev'] ** 2)
            pass_ratio_undergrad += stats['pass']
            count_undergrad += (stats['pass'] + stats['fail'])

        all_arr.append(stats['average'])
        all_std.append(stats['stdev'] ** 2)
        pass_ratio_all += stats['pass']
        count_all += (stats['pass'] + stats['fail'])

    calculate_undergrad_to_json(d, pass_ratio_undergrad, undergrad_arr, undergrad_std, count_undergrad)
    calculate_all_to_json(all_arr, all_std, d, pass_ratio_all, count_all)

    return d


def group_to_years(json_query):
    d = OrderedDict({})
    for query in json_query:
        stats = query['stats']
        year = query['year_session']
        try:
            course_no = int(query['course'])
        except ValueError:
            course_no = int(query['course'][0:3])

        if course_no >= 500 or stats['high'] == '':
            continue

        if year not in d:
            d[year] = {
                'average': [stats['average']],
                'high': stats['high'],
                'low': stats['low']
            }
        else:
            d[year]['average'].append(stats['average'])
            d[year]['high'] = max(d[year]['high'], stats['high'])
            d[year]['low'] = max(d[year]['low'], stats['low'])

    for year in d:
        d[year]['average'] = statistics.mean(d[year]['average'])

    return d
