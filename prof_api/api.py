import flask
from flask_restful import Api
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os

app = flask.Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
ma = Marshmallow(app)

import prof_api.filters as filters

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
api = Api(app)

api.add_resource(filters.Course, '/api/courses/<string:professor>')

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'
