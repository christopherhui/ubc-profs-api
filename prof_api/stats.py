from flask_restful import Resource
from flask import jsonify

from helper_functions import general_get, convert_to_general


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
        return general_get(professor,
                           'AND course.year_session = ? AND course.subject = ? AND course.course = ? AND course.section = ?',
                           year.upper(), subject.upper(), course, section, 'fetchone')


class generalStatistics(Resource):
    def get(self, professor):
        """

        :param professor:
        :return:
        """
        results = general_get(professor).json
        return jsonify(convert_to_general(results))
