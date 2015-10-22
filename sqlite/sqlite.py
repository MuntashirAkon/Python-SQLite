#!/usr/bin/python3
import sqlite3
from sqlite.sqlitestmt import SQLiteStmt
from sqlite.sqliteresult import SQLiteResult
from sqlite.sqliteexception import SQLiteException

__title__ = 'SQLite'
__version__ = '0.2.0'
__author__ = 'Muntashir Al-Islam'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2015 Muntashir Al-Islam'

"""
    The SQLite class

    date: 19/10/2015
"""


class SQLite(SQLiteException):
    """
    Represents a connection between Python3 and a SQLite3 database.
    """
    affected_rows = 0                          # Gets the number of affected rows in a previous SQLite operation
    connect_errno = ""                         # Returns the error code (error class) from last connect call
    connect_error = ""                         # Returns a string description of the last connect error
    client_info = sqlite3.version_info         # Get SQLite client info as a tuple
    client_version = sqlite3.version           # Returns the SQLite client version as a string
    field_count = 0                            # Returns the number of columns for the most recent query
    insert_id = 0                              # Returns the auto generated id used in the last query
    server_info = sqlite3.sqlite_version_info  # Returns the version of the SQLite as a tuple
    server_version = sqlite3.sqlite_version    # Returns the version of the SQLite as a string

    _options = dict()  # Save options when called SQLite.init()

    def __init__(self, file=''):
        """
        Open a new connection to the sqlite3
        :param file: SQLite DB file or :memory:
        :type file: str
        :rtype: None
        """
        if file != '':
            try:
                self._conn = sqlite3.connect(file)
                self._conn.isolation_level = None  # auto-commit is on
            except:
                import sys
                e = sys.exc_info()
                self.connect_errno = e[0]
                self.connect_error = e[1]

    def init(self):
        """
        Initializes SQLite and returns a resource for use with SQLite.real_connect()
        :rtype: SQLite
        """
        try:
            self._options['timeout'] = 5.0
            self._options['detect_types'] = 0
            self._options['isolation_level'] = None
            self._options['check_same_thread'] = False
            self._options['factory'] = None
            self._options['cached_statements'] = 100
        except:
            self._handle_error()
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
            self._handle_error()
            return False

    def begin_transaction(self):
        """
        Starts a transaction

        Note: sqlite3 module start transaction automatically on DML statements.
        So this function is kind of useless one.
        :rtype: bool
        """
        try:
            self._conn.cursor().execute("BEGIN")
            return True
        except:
            self._handle_error()
            return False

    def real_connect(self, file):
        """
        Opens a connection to a sqlite3 db
        :param file: SQLite DB file or :memory:
        :type file: str
        :rtype: bool
        """
        try:
            self._conn = sqlite3.connect(file, self._options['timeout'], self._options['detect_types'],
                                         self._options['isolation_level'], self._options['check_same_thread'],
                                         self._options['factory'], self._options['cached_statements'])
            return True
        except:
            import sys
            e = sys.exc_info()
            self.connect_errno = e[0]
            self.connect_error = e[1]
            return False

    def real_escape_string(self, escapestr):
        """
        Escapes special characters in a string for use in an SQL statement

        Note: unlike PHP, it does not depend on character set
        :param escapestr: a string that needs to be escaped
        :type escapestr: str
        :rtype: str or None
        """
        try:
            import re
            return re.escape(escapestr)
        except:
            self._handle_error()
            return None

    def escape_string(self, escapestr):
        """
        An alias of self.real_escape_string()
        :param escapestr: a string that needs to be escaped
        :type escapestr: str
        :rtype: str or None
        """
        return self.real_escape_string(escapestr)

    def get_client_info(self):
        """
        An alias of self.client_version
        :returns: self.client_version
        :rtype: str
        """
        return self.client_version

    def prepare(self, query):
        """
        Prepare an SQL statement for execution
        :param query: SQL query
        :type query: str
        :rtype: SQLiteStmt or bool
        """
        try:
            return self._query(query)
        except:
            self._handle_error()
            return False

    def query(self, query):  # todo: This  method should return SQLiteResult
        """
        Performs a query on the database
        :param query: SQL query
        :type query: str
        :rtype: SQLiteResult or bool
        """
        try:
            result = SQLiteResult(self._conn, query)
            return result
        except:
            self._handle_error()
            return False

    def rollback(self):
        """
        Rolls back current transaction
        :rtype: bool
        """
        try:
            self._conn.rollback()
            return True
        except:
            self._handle_error()
            return False

    def stmt_init(self):
        """
        Initializes a statement and returns an object for use with SQLiteStmt.prepare()
        :returns: SQLiteStmt without parameters meaning the SQLiteStmt.prepare() must be executed
        :rtype: SQLiteStmt or bool
        """
        try:
            return self._query()
        except:
            self._handle_error()
            return False

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
            self._handle_error()
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
            self._handle_error()
            return False

    def close(self):
        """
        Closes a previously opened database connection
        :rtype: bool
        """
        try:
            self._conn.close()
            return True
        except:
            self._handle_error()
            return False

    def kill(self):
        """
        Kill a SQLite transaction
        :return:
        """
        try:
            self._conn.interrupt()
            return True
        except:
            self._handle_error()
            return False

    def _query(self, query=''):
        """
        Switch to SQLiteStmt to execute and show result
        :rtype: SQLiteStmt or bool
        """
        try:
            return SQLiteStmt(self._conn, query)
        except:
            self._handle_error()
            return False
