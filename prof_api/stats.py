from flask_restful import Resource
from flask import jsonify, request

from prof_api.helper_functions import general_get, convert_to_general_overall, find_name


class allSessions(Resource):
    def get(self, professor):
        """

        :param professor: In forms of lines (i.e. Last-First)
        :return: all sessions that a professor has taught, including grade distributions and statistics
        """
        return general_get(find_name(professor))


class sessionsBySubject(Resource):
    def get(self, professor, subject):
        """

        :param professor: In forms of lines (i.e. Last-First)
        :param subject: course subject
        :return: all sessions that a professor has taught for a specific subject
        """
        return general_get(find_name(professor), 'AND course.subject = ?', subject.upper())


class sessionsByYear(Resource):
    def get(self, professor, year):
        """

        :param professor: In forms of lines (i.e. Last-First)
        :param year: year session
        :return: all sessions that professor has taught for some year
        """
        return general_get(find_name(professor), 'AND course.year_session = ?', year.upper())


class sessionsByYearFilterSubject(Resource):
    def get(self, professor, year, subject):
        """

        :param professor: In forms of lines (i.e. Last-First)
        :param year: year session
        :param subject: all sessions that professor has taught for some year
        :return: all sessions that a professor has taught
        """
        return general_get(find_name(professor), 'AND course.year_session = ? AND course.subject = ?',
                           year.upper(), subject.upper())


class courseByYearFilterSubjectSessions(Resource):
    def get(self, professor, year, subject, course):
        """

        :param professor: In forms of lines (i.e. Last-First)
        :param year:
        :param subject:
        :param course:
        :return:
        """
        return general_get(find_name(professor), 'AND course.year_session = ? AND course.subject = ? AND course.course = ?',
                           year.upper(), subject.upper(), course)


class sessionByYearFilterSubjectSession(Resource):
    def get(self, professor, year, subject, course, section):
        """
        Additional parameter added in, 'fetchone' to indicate that only
        session should be returned.
        :param professor: In forms of lines (i.e. Last-First)
        :param year:
        :param subject:
        :param course:
        :param section:
        :return:
        """
        return general_get(find_name(professor),
                           'AND course.year_session = ? AND course.subject = ? AND course.course = ? AND course.section = ?',
                           year.upper(), subject.upper(), course, section, 'fetchone')


class generalStatistics(Resource):
    def get(self, professor):
        """

        :param professor: In forms of lines (i.e. Last-First)
        :return:
        """
        results = general_get(find_name(professor)).json
        return jsonify(convert_to_general_overall(results))

    def post(self, professor):
        """

        :param professor: professor that has actually been in the correct format
        :return: general statistics about that professor
        """
        prof_name = request.json['prof']
        results = general_get(find_name(prof_name)).json
        return jsonify(convert_to_general_overall(results))


class generalStatisticsSubject(Resource):
    def get(self, professor, subject):
        results = general_get(find_name(professor), 'AND course.subject = ?', subject.upper()).json
        return jsonify(convert_to_general_overall(results))


class generalStatisticsSubjectCourse(Resource):
    def get(self, professor, subject, course):
        results = general_get(find_name(professor),
                              'AND course.subject = ? AND course.course = ?', subject.upper(), course).json
        return jsonify(convert_to_general_overall(results))


class generalStatisticsSubjectCourseYear(Resource):
    def get(self, professor, subject, course, year):
        results = general_get(find_name(professor),
                              'AND course.subject = ? AND course.course = ? AND course.year_session = ?',
                              subject.upper(), course, year.upper()).json
        return jsonify(convert_to_general_overall(results))

class generalStatisticsSubjectCourseYearSection(Resource):
    def get(self, professor, subject, course, year, section):
        results = general_get(find_name(professor),
                              'AND course.subject = ? AND course.course = ? AND course.year_session = ? AND course.section = ?',
                              subject.upper(), course, year.upper(), section).json
        return jsonify(convert_to_general_overall(results))