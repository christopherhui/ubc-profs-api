import requests
from database import Professor, Course, Grades, Stats, db

stats_cat = ['average', 'stdev', 'high', 'low', 'pass', 'fail', 'withdrew', 'audit', 'other']
grades_cat = ['0-9%', '10-19%', '20-29%', '30-39%', '40-49%', '<50%', '50-54%', '55-59%', '60-63%', '64-67%', '68-71%', '72-75%', '76-79%', '80-84%', '85-89%', '90-100%']

url = 'https://ubcgrades.com/api/'
years = requests.get(url + 'yearsessions')

for year in years.json():
    year_grades = requests.get(url + 'grades/' + year).json()
    for query in range(0, len(year_grades)):
        course = year_grades[query]
        if course['instructor'].strip(' ') != '':
            course_id = course['id']
            if db.session.query(Course.id).filter_by(course_id=course_id).scalar() is None:
                curr_course = Course(course_id=course_id, year_session=course['yearsession'], campus=course['campus'],
                                     subject=course['subject'], course=course['course'], section=course['section'],
                                     title=course['title'], enrolled=course['enrolled'])
                curr_grades = Grades(g0to9=course['grades'][grades_cat[0]], g10to19=course['grades'][grades_cat[1]], g20to29=course['grades'][grades_cat[2]],
                                     g30to39=course['grades'][grades_cat[3]], g40to49=course['grades'][grades_cat[4]], gless50=course['grades'][grades_cat[5]],
                                     g50to54=course['grades'][grades_cat[6]], g55to59=course['grades'][grades_cat[7]], g60to63=course['grades'][grades_cat[8]],
                                     g64to67=course['grades'][grades_cat[9]], g68to71=course['grades'][grades_cat[10]], g72to75=course['grades'][grades_cat[11]]
                                     , g76to79=course['grades'][grades_cat[12]], g80to84=course['grades'][grades_cat[13]], g85to89=course['grades'][grades_cat[14]],
                                     g90to100=course['grades'][grades_cat[15]], course=curr_course)
                curr_stats = Stats(average=course['stats'][stats_cat[0]], stdev=course['stats'][stats_cat[1]], high=course['stats'][stats_cat[2]],
                                   low=course['stats'][stats_cat[3]], passed=course['stats'][stats_cat[4]], fail=course['stats'][stats_cat[5]],
                                   withdrew=course['stats'][stats_cat[6]], audit=course['stats'][stats_cat[7]], other=course['stats'][stats_cat[8]], course=curr_course)
                db.session.add(curr_course)
                db.session.add(curr_grades)
                db.session.add(curr_stats)
                print('added course for {} in year {}'.format(curr_course.course_id, curr_course.year_session))
            else:
                curr_course = Course.query.filter_by(course_id=course_id).first()
                print('queried course for {} in year {}'.format(curr_course.course_id, curr_course.year_session))
            instructors = course['instructor'].split(';')
            for instructor_name in instructors:
                if db.session.query(Professor.id).filter_by(name=instructor_name).scalar() is None:
                    curr_professor = Professor(name=instructor_name)
                    db.session.add(curr_professor)
                else:
                    curr_professor = Professor.query.filter_by(name=instructor_name).first()
                curr_course.professors.append(curr_professor)
                print('added professor named {} for course {} in year {}'.format(curr_professor.name, curr_course.course_id, curr_course.year_session))
            db.session.commit()
        db.session.commit()
    db.session.commit()