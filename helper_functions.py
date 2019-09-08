import math
import sqlite3
import re

from flask import jsonify

from api import app

stats_cat = ["average", "stdev", "high", "low", "passed", "fail", "withdrew", "audit", "other"]
grades_cat = {"g0to9": "0-9%", "g10to19": "10-19%", "g20to29": "20-29%", "g30to39": "30-39%", "g40to49": "40-49%", "gless50": "<50%", "g50to54": "50-54%", "g55to59": "55-59%", "g60to63": "60-63%", "g64to67": "64-67%", "g68to71": "68-71%", "g72to75": "72-75%", "g76to79": "76-79%", "g80to84": "80-84%", "g85to89": "85-89%", "g90to100": "90-100%"}
yearsessions = ["1996S", "1996W", "1997S", "1997W", "1998S", "1998W", "1999S", "1999W", "2000S", "2000W", "2001S", "2001W", "2002S", "2002W", "2003S", "2003W", "2004S", "2004W", "2005S", "2005W", "2006S", "2006W", "2007S", "2007W", "2008S", "2008W", "2009S", "2009W", "2010S", "2010W", "2011S", "2011W", "2012S", "2012W", "2013S", "2013W", "2014S", "2014W", "2015S", "2015W", "2016S", "2016W", "2017S", "2017W", "2018S", "2018W"]
subjects = ["AANB", "ACAM", "ADED", "ADHE", "AFST", "AGEC", "AGRO", "AGSC", "ANAE", "ANAT", "ANSC", "ANTH", "APBI", "APPP", "APSC", "ARBC", "ARCH", "ARCL", "ARST", "ARTE", "ARTH", "ARTS", "ASIA", "ASIC", "ASTR", "ASTU", "ATSC", "AUDI", "BA", "BAAC", "BABS", "BAEN", "BAFI", "BAHC", "BAHR", "BAIM", "BAIT", "BALA", "BAMA", "BAMS", "BAPA", "BASC", "BASD", "BASM", "BATL", "BATM", "BAUL", "BIOC", "BIOE", "BIOF", "BIOL", "BMEG", "BOTA", "BRDG", "BUED", "BUSI", "CAPS", "CCFI", "CCST", "CDSC", "CDST", "CEEN", "CELL", "CENS", "CHBE", "CHEM", "CHIL", "CHIN", "CHML", "CICS", "CIVL", "CLCH", "CLST", "CNPS", "CNRS", "CNTO", "COEC", "COGS", "COHR", "COML", "COMM", "COMR", "CONS", "CPEN", "CPSC", "CRWR", "CSED", "CSIS", "CSPW", "CUST", "DANI", "DENT", "DERM", "DHYG", "DMED", "DPAS", "DRAM", "DSCI", "EADM", "ECED", "ECON", "EDCI", "EDCP", "EDST", "EDUC", "EECE", "ELEC", "EMBA", "EMER", "ENDS", "ENED", "ENGL", "ENPH", "ENVR", "EOSC", "EPSE", "ERTH", "ETEC", "EXCH", "FACT", "FDNS", "FEBC", "FHIS", "FILM", "FINA", "FIPR", "FISH", "FIST", "FMED", "FMPR", "FMSC", "FMST", "FNEL", "FNH", "FNIS", "FNLG", "FNSP", "FOOD", "FOPR", "FPEN", "FRE", "FREN", "FRSI", "FRST", "GBPR", "GEM", "GENE", "GEOB", "GEOG", "GEOL", "GEOP", "GEPA", "GERM", "GPP", "GREK", "GRS", "GRSJ", "GSAT", "HCEC", "HCEP", "HCET", "HEBR", "HECO", "HESO", "HGSE", "HIED", "HIND", "HINU", "HIST", "HKIN", "HMEC", "HMED", "HPB", "HUNU", "HXAH", "HXDR", "HXEC", "HXEN", "HXFL", "HXFR", "HXGM", "HXGY", "HXHI", "HXMA", "HXMU", "HXPC", "HXPH", "HXPS", "HXPY", "HXRE", "HXSP", "HXWR", "IAR", "IEST", "IGEN", "IHHS", "INDE", "INDO", "INDS", "INFO", "INLB", "ISCI", "ITAL", "ITST", "IWME", "JAPN", "JRNL", "KIN", "KORN", "LAIS", "LANE", "LARC", "LASO", "LAST", "LATN", "LAW", "LFS", "LIBE", "LIBR", "LING", "LLED", "LWS", "MAED", "MATH", "MDVL", "MECH", "MEDD", "MEDG", "MEDH", "MEDI", "MGMT", "MICB", "MIDW", "MINE", "MLED", "MMAT", "MMPE", "MRNE", "MTRL", "MUED", "MUSC", "NAME", "NEST", "NRSC", "NURS", "OBMS", "OBST", "OCCH", "OCGY", "OHS", "OMSS", "ONCO", "OPTH", "ORBI", "ORNT", "ORPA", "OSOT", "PAED", "PATH", "PCTH", "PERS", "PETE", "PHAR", "PHIL", "PHRM", "PHTH", "PHYL", "PHYS", "PLAN", "PLNT", "POLI", "POLS", "PORT", "PPEN", "PRIN", "PSYC", "PSYT", "PUNJ", "RADI", "READ", "RELG", "RES", "RGLA", "RGLT", "RHSC", "RMES", "RMST", "RSOT", "RSPT", "RUSS", "SANS", "SCAN", "SCED", "SCIE", "SEAL", "SLAV", "SOAL", "SOCI", "SOIL", "SOWK", "SPAN", "SPHA", "SPPH", "SSED", "STAT", "STS", "SURG", "SWED", "SWFS", "THTR", "TIBT", "TSED", "UDES", "UFOR", "URDU", "URO", "URST", "URSY", "VANT", "VISA", "VRHC", "WMST", "WOOD", "WRDS", "WRIT", "ZOOL"]


def find_name(professor):
    """
    Takes a name from webpage and makes it possible to query in the database

    :param professor: name of professor in dash form
    :return: name of professor used for querying database and '' if not found
    """
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
    d = {}
    d["grades"] = {}
    d["stats"] = {}
    for idx, col in enumerate(cursor.description):
        if col[0] == "id" or col[0] == "course_id":
            continue
        elif col[0] in grades_cat:
            d["grades"][grades_cat[col[0]]] = row[idx]
        elif col[0] in stats_cat:
            if col[0] == "passed":
                d["stats"]["pass"] = row[idx]
            else:
                d["stats"][col[0]] = row[idx]
        else:
            d[col[0]] = row[idx]
    return d


def general_get(professor, add_query='', *options):
    """
    General function for querying in database for professor and returning
    JSON formatted result

    :param professor:
    :param add_query:
    :param options:
    :return:
    """
    query = 'SELECT course.*, stats.*, grades.* FROM professor ' \
            'INNER JOIN association ON professor.id = association.professor_id ' \
            'INNER JOIN course ON course.id = association.course_id ' \
            'INNER JOIN stats ON course.id=stats.course_id ' \
            'INNER JOIN grades ON course.id = grades.course_id ' \
            'WHERE professor.name = ? ' + add_query

    conn = sqlite3.connect(app.config['DATABASE_NAME'])
    conn.row_factory = result_to_json
    cur = conn.cursor()
    new_professor = find_name(professor)
    new_options = [new_professor] + [x for x in options if x != 'fetchone']
    if 'fetchone' in options:
        results = cur.execute(query, new_options).fetchone()
    else:
        results = cur.execute(query, new_options).fetchall()

    return jsonify(results)


def convert_to_general(json_query):
    """
    Given a JSON query, typically with multiple courses, returns the
    general statistics of all courses under which the JSON query contains
    :param json_query:
    :return:
    """
    if len(json_query) == 0:
        return {}

    d = {}
    d["undergrad"] = {}
    d["all"] = {}
    d["undergrad"]["grades"] = {}
    d["all"]["grades"] = {}

    average_undergrad = 0
    standard_deviation_undergrad = 0
    pass_ratio_undergrad = 0
    courses_undergrad = 0

    average_all = 0
    standard_deviation_all = 0
    pass_ratio_all = 0
    courses_all = len(json_query)

    for query in json_query:
        grades = query["grades"]
        stats = query["stats"]

        # Attempts to find whether or the course has an additional letter at the end
        # If it does, then we will use the condensed version
        try:
            course_no = int(query["course"])
        except ValueError:
            course_no = int(query["course"][0:2])

        # Check that there are actually statistics for this course before adding values in
        if stats["average"] == "":
            courses_all -= 1
            continue

        for grade_bound, grade in grades.items():
            if grade_bound not in d["all"]["grades"]:
                d["all"]["grades"][grade_bound] = grade
            else:
                d["all"]["grades"][grade_bound] += grade

            if course_no < 500:
                if grade_bound not in d["undergrad"]["grades"]:
                    d["undergrad"]["grades"][grade_bound] = grade
                else:
                    d["undergrad"]["grades"][grade_bound] += grade

        if course_no < 500:
            average_undergrad += stats["average"]
            standard_deviation_undergrad += stats["stdev"] ** 2
            pass_ratio_undergrad += stats["pass"]/(stats["pass"] + stats["fail"])
            courses_undergrad += 1
        average_all += stats["average"]
        standard_deviation_all += stats["stdev"] ** 2
        pass_ratio_all += stats["pass"]/(stats["pass"] + stats["fail"])

    d["undergrad"]["average"] = "" if courses_undergrad == 0 else round(average_undergrad / courses_undergrad, 2)
    d["undergrad"]["stdev"] = "" if courses_undergrad == 0 else round(math.sqrt(standard_deviation_undergrad / courses_undergrad), 2)
    d["undergrad"]["pass"] = "" if courses_undergrad == 0 else round(pass_ratio_undergrad / courses_undergrad, 2)

    d["all"]["average"] = round(average_all / courses_all, 2)
    d["all"]["stdev"] = round(math.sqrt(standard_deviation_all / courses_all), 2)
    d["all"]["pass"] = round(pass_ratio_all / courses_all, 2)
    return d
