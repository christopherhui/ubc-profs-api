from flask_restful import Resource, Api
from flask import jsonify
import sqlite3
import re
from prof_api.api import app

class Course(Resource):
    def get(self, professor):
        query = 'SELECT DISTINCT course.subject ' \
            'FROM professor JOIN association ON professor.id = association.professor_id JOIN course ON course.id = association.course_id ' \
            'WHERE professor.name = ? COLLATE NOCASE;'

        conn = sqlite3.connect(app.config['DATABASE_NAME'])
        cur = conn.cursor()
        new_professor = find_name(professor)
        results = cur.execute(query, [new_professor]).fetchall()
        new_results = [result[0] for result in results]

        return jsonify(new_results)

class Subject(Resource):
    def get(self, professor, subject):
        pass

class Year(Resource):
    def get(self, professor, year):
        pass

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