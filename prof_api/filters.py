from flask_restful import Resource, Api
from flask import jsonify
import sqlite3
from prof_api.api import app

# Todo: Work on using regex to search for professor

class Course(Resource):
    def get(self, professor):
        q = 'SELECT DISTINCT course.subject ' \
            'FROM professor JOIN association ON professor.id = association.professor_id JOIN course ON course.id = association.course_id ' \
            'WHERE professor.name = ? COLLATE NOCASE;'

        conn = sqlite3.connect(app.config['DATABASE_NAME'])
        cur = conn.cursor()
        new_professor = parse_name(professor)
        results = cur.execute(q, [new_professor]).fetchall()
        new_results = [result[0] for result in results]

        return jsonify(new_results)

class Subject(Resource):
    def get(self, professor, subject):
        pass

class Year(Resource):
    def get(self, professor, year):
        pass

def parse_name(professor):
    """

    :param professor: full name of professor
    :return: parsed version in form of lastname-firstname
    """
    name = professor.split('-')
    if len(name) == 1:
        return name[0]
    else:
        return name[0] + ', ' + ' '.join([name[i] for i in range(1, len(name))])
