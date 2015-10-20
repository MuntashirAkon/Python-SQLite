#!/usr/bin/python3

import sqlite3
from sqlite.sqlitestmt import SQLiteStmt

__title__ = 'SQLite'
__version__ = '0.1.0'
__author__ = 'Muntashir Al-Islam'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2015 Muntashir Al-Islam'

"""
    The SQLite class

    date: 19/10/2015
"""


class SQLite:
    """
    Represents a connection between Python3 and a SQLite3 database.
    """
    _options = dict()

    def __init__(self, file=''):
        """
        Open a new connection to the sqlite3
        :param file: SQLite DB file or :memory:
        :type file: str
        :rtype: None
        """
        if file != '':
            self._conn = sqlite3.connect(file)
            self._conn.isolation_level = None
        self.server_version = sqlite3.sqlite_version  # Returns the version of the SQLite as a STRING
        self.server_info = sqlite3.sqlite_version_info  # Returns the version of the MySQL server as a TUPLE

    def init(self):
        """
        Initializes SQLite and returns a resource for use with SQLite.real_connect()
        :rtype: SQLite
        """
        self._options['timeout'] = 5.0
        self._options['detect_types'] = 0
        self._options['isolation_level'] = None
        self._options['check_same_thread'] = False
        self._options['factory'] = None
        self._options['cached_statements'] = 100
        return self

    def options(self, option, value):
        """
        Set options
        NOTE: Unlike mysqli::options there are option and value argument
        These arguments are related to the sqlite3.connect module
        :param option: "timeout", "detect_types", "isolation_level", "check_same_thread", "factory", "cached_statements"
        :type option: str
        :param value: defaults (5.0, 0, None, False, None, 100)
        :type value: bool or int or float or None
        :rtype: bool
        """
        try:
            self._options[option] = value
            return True
        except:
            return False

    def real_connect(self, file):
        """
        Opens a connection to a sqlite3 db
        :param file: SQLite DB file or :memory:
        :type file: str
        :rtype: bool
        """
        try:
            self._conn = sqlite3.connect(file, self._options['timeout'], self._options['detect_types'], self._options['isolation_level'], self._options['check_same_thread'], self._options['factory'], self._options['cached_statements'])
            return True
        except:
            return False

    def prepare(self, query):
        """
        Prepare an SQL statement for execution
        :param query: SQL query
        :type query: str
        :rtype: SQLiteStmt
        """
        return self._query(query)

    def query(self, query):  # todo: This  method should return SQLiteResult
        """
        Performs a query on the database
        Note: This method should not return SQLiteStmt. This problem will be solved in future realise
        :param query: SQL query
        :type query: str
        :rtype: SQLiteStmt
        """
        return self._query(query)

    def stmt_init(self):
        """
        Initializes a statement and returns an object for use with SQLiteStmt.prepare()
        :returns: SQLiteStmt without parameters meaning the SQLiteStmt.prepare() must be executed
        :rtype: SQLiteStmt
        """
        return self._query()

    def autocommit(self, mode=None):
        """
        Turns on or off auto-committing database modifications
        NOTE: mode can take any value that isolation_level can have
        :param mode: default is None (means True)
        :type mode: str or None
        :rtype: bool
        """
        try:
            self._conn.isolation_level = mode
            return True if not mode else False
        except:
            return False

    def commit(self):
        """
        Commits the current transaction
        :rtype: bool
        """
        try:
            self._conn.commit()
            return True
        except:
            return False

    def close(self):
        """
        Closes a previously opened database connection
        :rtype: bool
        """
        try:
            self._conn.close()
        except:
            return False

    def _query(self, query=''):
        """
        Switch to SQLiteStmt to execute and show result
        :rtype: SQLiteStmt
        """
        return SQLiteStmt(self._conn, query)
