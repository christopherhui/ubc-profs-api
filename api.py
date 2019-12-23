import flask
from flask_restful import Api
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os

app = flask.Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
ma = Marshmallow(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
api = Api(app)

import prof_api.filters as filters

api.add_resource(filters.Course, '/api/courses/<string:professor>')
api.add_resource(filters.Subject, '/api/subjects/<string:professor>/<string:subject>')
api.add_resource(filters.Year, '/api/courses/<string:professor>/<string:subject>/<string:course>')
api.add_resource(filters.Professors, '/api/professors')

import prof_api.stats as stats

api.add_resource(stats.allSessions, '/api/stats/<string:professor>')
api.add_resource(stats.sessionsByYear, '/api/stats/<string:professor>/<string:year>')
api.add_resource(stats.sessionsByYearFilterSubject, '/api/stats/<string:professor>/<string:year>/<string:subject>')
api.add_resource(stats.courseByYearFilterSubjectSessions, '/api/stats/<string:professor>/<string:year>/<string:subject>/<string:course>')
api.add_resource(stats.sessionByYearFilterSubjectSession, '/api/stats/<string:professor>/<string:year>/<string:subject>/<string:course>/<string:section>')
api.add_resource(stats.generalStatistics, '/api/general-stats/<string:professor>')

api.add_resource(stats.sessionsBySubject, '/api/stats/subject/<string:professor>/<string:subject>')

@app.route('/')
def home():
    return flask.render_template('home.html')

@app.route('/courses')
def courses():
    return flask.render_template('courses.html')
