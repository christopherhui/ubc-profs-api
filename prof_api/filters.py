from flask_restful import Resource
from flask import jsonify, request
import sqlite3
from api import app
from prof_api.helper_functions import find_name


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
                'WHERE professor.name = ? AND course.subject = ?;'

        conn = sqlite3.connect(app.config['DATABASE_NAME'])
        cur = conn.cursor()
        new_professor = find_name(professor)
        results = cur.execute(query, [new_professor, subject.upper()]).fetchall()
        new_results = [result[0] for result in results]

        return jsonify(new_results)


class Year(Resource):
    def get(self, professor, subject, course):
        """

        :param professor: professor's name
        :param subject:
        :param course:
        :return: all years sessions of when a professor has taught
        """
        query = 'SELECT DISTINCT course.year_session ' \
                'FROM professor JOIN association ON professor.id = association.professor_id JOIN course ' \
                'ON course.id = association.course_id ' \
                'WHERE professor.name = ? AND course.subject = ? AND course.course = ?;'

        conn = sqlite3.connect(app.config['DATABASE_NAME'])
        cur = conn.cursor()
        new_professor = find_name(professor)
        results = cur.execute(query, [new_professor, subject.upper(), course]).fetchall()
        new_results = [result[0] for result in results]

        return jsonify(new_results)


class Section(Resource):
    def get(self, professor, subject, course, year):
        """

        :param professor: professor's name
        :param subject:
        :param course:
        :param year:
        :return: all years sessions of when a professor has taught
        """
        query = 'SELECT DISTINCT course.section ' \
                'FROM professor JOIN association ON professor.id = association.professor_id JOIN course ' \
                'ON course.id = association.course_id ' \
                'WHERE professor.name = ? AND course.subject = ? AND course.course = ? AND course.year_session = ?;'

        conn = sqlite3.connect(app.config['DATABASE_NAME'])
        cur = conn.cursor()
        new_professor = find_name(professor)
        results = cur.execute(query, [new_professor, subject.upper(), course, year]).fetchall()
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

    def post(self):
        """

        :return: list of all professor names with wildcard guesses, only 5 professors returned maximum
        """
        prof_name = request.json["prof"]

        query = 'SELECT professor.name FROM professor WHERE professor.name LIKE ?' \
                'ORDER by professor.name'

        conn = sqlite3.connect(app.config['DATABASE_NAME'])
        cur = conn.cursor()

        if len(prof_name.split(' ')) > 1:
            space_prof_name = prof_name.replace(' ', '%')
            reversed_prof_name = '%'.join(reversed(prof_name.split(' ')))
            results1 = cur.execute(query, ['%' + space_prof_name + '%']).fetchall()
            results2 = cur.execute(query, ['%' + reversed_prof_name + '%']).fetchall()

            results = results1 if len(results1) > len(results2) else results2

        else:
            results = cur.execute(query, ['%' + prof_name + '%']).fetchall()

        return jsonify(results) if len(results) <= 5 else jsonify(results[0:5])
