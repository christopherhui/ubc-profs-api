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
api.add_resource(filters.Year, '/api/courses/<string:professor>/<string:year>')

import prof_api.stats as stats

api.add_resource(stats.allCourses, '/api/<string:professor>')

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'
