from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

association = db.Table('association',
                       db.Column('professor_id', db.Integer, db.ForeignKey('professor.id'),primary_key=True),
                       db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True))

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    courses = db.relationship('Course', secondary=association, backref=db.backref('professors', lazy=True), lazy=True)

    def __repr__(self):
        return f"Professor('{self.name}')"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String, nullable=False)
    year_session = db.Column(db.String(10), nullable=False)
    campus = db.Column(db.String(10))
    subject = db.Column(db.String)
    course = db.Column(db.String)
    section = db.Column(db.Integer)
    title = db.Column(db.String)
    enrolled = db.Column(db.Integer)
    grades = db.relationship('Grades', backref='course', uselist=False, lazy=True)
    stats = db.relationship('Stats', backref='course', uselist=False, lazy=True)

    def __repr__(self):
        return f"Course('{self.name}', '{self.year_session}', '{self.section}', '{self.campus}'," \
            f" '{self.subject}', '{self.course}', '{self.section}', '{self.title}', '{self.enrolled}')"

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    g0to9 = db.Column(db.Integer)
    g10to19 = db.Column(db.Integer)
    g20to29 = db.Column(db.Integer)
    g30to39 = db.Column(db.Integer)
    g40to49 = db.Column(db.Integer)
    gless50 = db.Column(db.Integer)
    g50to54 = db.Column(db.Integer)
    g55to59 = db.Column(db.Integer)
    g60to63 = db.Column(db.Integer)
    g64to67 = db.Column(db.Integer)
    g68to71 = db.Column(db.Integer)
    g72to75 = db.Column(db.Integer)
    g76to79 = db.Column(db.Integer)
    g80to84 = db.Column(db.Integer)
    g85to89 = db.Column(db.Integer)
    g90to100 = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def __repr__(self):
        return f"Grades('{self.g0to9}', '{self.g10to19}', '{self.g20to29}', '{self.g30to39}', '{self.g40to49}', " \
            f"'{self.gless50}', '{self.g50to54}', '{self.g55to59}', '{self.g60to63}', '{self.g64to67}', '{self.g68to71}'," \
            f" '{self.g72to75}', '{self.g76to79}', '{self.g80to84}', '{self.g85to89}', '{self.g90to100}')"

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    average = db.Column(db.Integer)
    stdev = db.Column(db.Integer)
    high = db.Column(db.Integer)
    low = db.Column(db.Integer)
    passed = db.Column(db.Integer)
    fail = db.Column(db.Integer)
    withdrew = db.Column(db.Integer)
    audit = db.Column(db.Integer)
    other = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def __repr__(self):
        return f"Stats('{self.average}', '{self.stdev}', '{self.high}', '{self.low}', '{self.passed}', '{self.fail}'," \
            f" '{self.withdrew}', '{self.audit}', '{self.other}')"

# Professor Schema
class ProfessorSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'courses')

# Init schema
professor_schema = ProfessorSchema(strict=True)
professors_schema = ProfessorSchema(many=True, strict=True)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
