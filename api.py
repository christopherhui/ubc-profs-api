import flask
from flask_restful import Api
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import prof_api.filters as filters
import os

app = flask.Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
ma = Marshmallow(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
api = Api(app)

api.add_resource(filters.Course, '/api/courses/<string:professor>')
api.add_resource(filters.Subject, '/api/subjects/<string:professor>/<string:subject>')
api.add_resource(filters.Year, '/api/years/<string:professor>/<string:subject>/<string:course>')
api.add_resource(filters.Section, '/api/sections/<string:professor>/<string:subject>/<string:course>/<string:year>')
api.add_resource(filters.Professors, '/api/professors')
api.add_resource(filters.SubjectFindCourses, '/api/subjects/courses/<string:subject>')
api.add_resource(filters.SubjectCourseProfessor, '/api/professors/<string:subject>/<string:course>')

import prof_api.stats as stats

api.add_resource(stats.allSessions, '/api/stats/<string:professor>')
api.add_resource(stats.sessionsByYear, '/api/stats/<string:professor>/<string:year>')
api.add_resource(stats.sessionsByYearFilterSubject, '/api/stats/<string:professor>/<string:year>/<string:subject>')
api.add_resource(stats.courseByYearFilterSubjectSessions, '/api/stats/<string:professor>/<string:year>/<string:subject>/<string:course>')
api.add_resource(stats.sessionByYearFilterSubjectSession, '/api/stats/<string:professor>/<string:year>/<string:subject>/<string:course>/<string:section>')

api.add_resource(stats.sessionsBySubject, '/api/stats/subject/<string:professor>/<string:subject>')
api.add_resource(stats.generalStatisticsByYear, '/api/stats/years/<string:professor>')

api.add_resource(stats.generalStatistics, '/api/general-stats/<string:professor>')
api.add_resource(stats.generalStatisticsVerbose, '/api/general-stats-verbose/<string:professor>')
api.add_resource(stats.generalStatisticsVerboseByCourse, '/api/general-stats-verbose/<string:professor>/<string:subject>/<string:course>')
api.add_resource(stats.generalStatisticsSubject, '/api/general-stats/<string:professor>/<string:subject>')
api.add_resource(stats.generalStatisticsSubjectCourse, '/api/general-stats/<string:professor>/<string:subject>/<string:course>')
api.add_resource(stats.generalStatisticsSubjectCourseYear, '/api/general-stats/<string:professor>/<string:subject>/<string:course>/<string:year>')
api.add_resource(stats.generalStatisticsSubjectCourseYearSection, '/api/general-stats/<string:professor>/<string:subject>/<string:course>/<string:year>/<string:section>')

@app.route('/')
def home():
    return flask.render_template('home.html')

@app.route('/courses')
def courses():
    return flask.render_template('courses.html')

@app.route('/date')
def date():
    return flask.render_template('date.html')

@app.route('/course-comparator')
def course_comparator():
    return flask.render_template('course-selector.html')

@app.route('/about')
def about():
    return flask.render_template('about.html')

if __name__ == "__main__":
    app.debug = True
    app.config['DATABASE_NAME'] = 'db.sqlite'
    host = os.environ.get('IP', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)

