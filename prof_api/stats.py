from flask_restful import Resource
from flask import jsonify
import sqlite3
from api import app
from helper_functions import find_name, result_to_json

def general_get(professor, add_query='', *options):
    query = 'SELECT course.*, stats.*, grades.* FROM professor ' \
            'INNER JOIN association ON professor.id = association.professor_id ' \
            'INNER JOIN course ON course.id = association.course_id ' \
            'INNER JOIN stats ON course.id=stats.course_id ' \
            'INNER JOIN grades ON course.id = grades.course_id ' \
            'WHERE professor.name = ? ' + add_query

    conn = sqlite3.connect(app.config['DATABASE_NAME'])
    conn.row_factory = result_to_json
    cur = conn.cursor()
    new_professor = find_name(professor)
    new_options = [new_professor] + [x for x in options if x != 'fetchone']
    if 'fetchone' in options:
        results = cur.execute(query, new_options).fetchone()
    else:
        results = cur.execute(query, new_options).fetchall()

    return jsonify(results)

class allSessions(Resource):
    def get(self, professor):
        """

        :param professor: name of the professor
        :return: all sessions that a professor has taught, including grade distributions and statistics
        """
        return general_get(professor)

class sessionsBySubject(Resource):
    def get(self, professor, subject):
        """

        :param professor: name of the professor
        :param subject: course subject
        :return: all sessions that a professor has taught for a specific subject
        """
        return general_get(professor, 'AND course.subject = ?', subject.upper())

class sessionsByYear(Resource):
    def get(self, professor, year):
        """

        :param professor: name of the professor
        :param year: year session
        :return: all sessions that professor has taught for some year
        """
        return general_get(professor, 'AND course.year_session = ?', year.upper())

class sessionsByYearFilterSubject(Resource):
    def get(self, professor, year, subject):
        """

        :param professor: name of the professor
        :param year: year session
        :param subject: all sessions that professor has taught for some year
        :return: all sessions that a professor has taught
        """
        return general_get(professor, 'AND course.year_session = ? AND course.subject = ?',
                           year.upper(), subject.upper())

class courseByYearFilterSubjectSessions(Resource):
    def get(self, professor, year, subject, course):
        """

        :param professor:
        :param year:
        :param subject:
        :param course:
        :return:
        """
        return general_get(professor, 'AND course.year_session = ? AND course.subject = ? AND course.course = ?',
                           year.upper(), subject.upper(), course)

class sessionByYearFilterSubjectSession(Resource):
    def get(self, professor, year, subject, course, section):
        """
        Additonal parameter added in, 'fetchone' to indicate that only
        session should be returned.
        :param professor:
        :param year:
        :param subject:
        :param course:
        :param section:
        :return:
        """
        return general_get(professor, 'AND course.year_session = ? AND course.subject = ? AND course.course = ? AND course.section = ?',
                           year.upper(), subject.upper(), course, section, 'fetchone')