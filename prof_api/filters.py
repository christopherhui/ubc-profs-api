from flask_restful import Resource
from flask import jsonify
import sqlite3
from api import app
from helper_functions import find_name

class Course(Resource):
    def get(self, professor):
        """

        :param professor: professor's name
        :return: all courses a professor has taught
        """
        query = 'SELECT DISTINCT course.subject ' \
            'FROM professor JOIN association ON professor.id = association.professor_id JOIN course ' \
                'ON course.id = association.course_id ' \
                'WHERE professor.name = ? COLLATE NOCASE;'

        conn = sqlite3.connect(app.config['DATABASE_NAME'])
        cur = conn.cursor()
        new_professor = find_name(professor)
        results = cur.execute(query, [new_professor]).fetchall()
        new_results = [result[0] for result in results]

        return jsonify(new_results)

class Subject(Resource):
    def get(self, professor, subject):
        """

        :param professor: professor's name
        :param subject: specific course (i.e. STAT, ENGL)
        :return: subject of a course (i.e. 100, 320)
        """
        query = 'SELECT DISTINCT course.course ' \
            'FROM professor JOIN association ON professor.id = association.professor_id JOIN course ' \
                'ON course.id = association.course_id ' \
                'WHERE professor.name = ? AND course.subject = ? COLLATE NOCASE;'

        conn = sqlite3.connect(app.config['DATABASE_NAME'])
        cur = conn.cursor()
        new_professor = find_name(professor)
        results = cur.execute(query, [new_professor, subject]).fetchall()
        new_results = [result[0] for result in results]

        return jsonify(new_results)

class Year(Resource):
    def get(self, professor, year):
        """

        :param professor: professor's name
        :param year: year session of when a professor has taught
        :return: all course subjects for a specific year
        """
        query = 'SELECT DISTINCT course.subject ' \
                'FROM professor JOIN association ON professor.id = association.professor_id JOIN course ' \
                'ON course.id = association.course_id ' \
                'WHERE professor.name = ? AND course.year_session = ? COLLATE NOCASE;'

        conn = sqlite3.connect(app.config['DATABASE_NAME'])
        cur = conn.cursor()
        new_professor = find_name(professor)
        results = cur.execute(query, [new_professor, year]).fetchall()
        new_results = [result[0] for result in results]

        return jsonify(new_results)

class Professors(Resource):
    def get(self):
        """

        :return: list of all professor names
        """
        query = 'SELECT professor.name FROM professor'

        conn = sqlite3.connect(app.config['DATABASE_NAME'])
        cur = conn.cursor()
        results = cur.execute(query).fetchall()
        new_results = [result[0] for result in results]

        return jsonify(new_results)
