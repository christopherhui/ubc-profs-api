from flask_restful import Resource, Api
from flask import jsonify
import sqlite3
from prof_api.api import app
from helper_functions import find_name, result_to_json

class allCourses(Resource):
    def get(self, professor):
        """

        :param professor: name of the professor
        :return: all courses that a professor has taught, including grade distributions and statistics
        """
        query = 'SELECT course.*, stats.*, grades.* FROM professor ' \
                'INNER JOIN association ON professor.id = association.professor_id ' \
                'INNER JOIN course ON course.id = association.course_id ' \
                'INNER JOIN stats ON course.id=stats.course_id ' \
                'INNER JOIN grades ON course.id = grades.course_id ' \
                'WHERE professor.name = ?'

        conn = sqlite3.connect(app.config['DATABASE_NAME'])
        conn.row_factory = result_to_json
        cur = conn.cursor()
        new_professor = find_name(professor)
        results = cur.execute(query, [new_professor]).fetchall()

        return jsonify(results)