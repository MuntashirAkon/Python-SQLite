#!/usr/bin/python3

__title__ = 'SQLiteStmt'
__version__ = '0.1.0'
__author__ = 'Muntashir Al-Islam'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2015 Muntashir Al-Islam'

"""
    The SQLiteStmt class

    date: 19/10/2015
"""

class SQLiteStmt:
    """
    Represents a prepared statement.
    """
    num_rows = 0  # Return the number of rows in statements result set
    affected_rows = 0  # Returns the total number of rows changed, deleted, or inserted by the last executed statement
    param_count = 0  # Returns the number of parameter for the given statement
    insert_id = 0  # Get the ID generated from the previous INSERT operation
    _params = tuple()
    _store_result = False
    _fetched_rows = list()
    _temp_index = 0
    _bind_args = tuple()

    def __init__(self, conn, query=''):
        """
        Constructs a new SQLiteStmt object
        :param conn: sqlite3.connect object
        :type conn: sqlite3.connect
        :param query: SQL query
        :type query: str
        :rtype: None
        """
        self._conn = conn
        self._query = query
        self.param_count = query.count('?')

    def prepare(self, query):
        """
        Prepare an SQL statement for execution
        :param query: SQL query
        :type query: str
        :rtype: bool
        """
        try:
            self._query = query
            self.param_count = query.count('?')
            return True
        except:
            return False

    def bind_param(self, types, *args):
        """
        Binds variables to a prepared statement as parameters
        :param types: does nothing. it's kept just for the accustomed php developer
        :param args: values
        :rtype: bool
        """
        try:
            del types
            self._params = args
            return True
        except:
            return False

    def bind_result(self, *args):
        """
        Binds (list/immutable) variables to a prepared statement for result storage
        NOTE: the arguments must be a list() due to certain limitations in python
        :param args: list() variables e.g: stmt.bind_result(list1, list2)
        :type args: list
        :rtype: bool
        """
        try:
            self._bind_args = args
            return True
        except:
            return False

    def execute(self):
        """
        Executes a prepared Query
        :rtype: bool
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(self._query, self._params)
            if self._conn.isolation_level:
                self._conn.commit()
            rows = cursor.fetchall()  # fetch all the rows

            self.affected_rows = cursor.rowcount if cursor.rowcount != -1 else 0  # affected rows is either .rowcount or 0
            self.num_rows = len(rows)
            if cursor.lastrowid:
                self.insert_id = cursor.lastrowid
            if self.num_rows > 0:
                self._fetched_rows = rows
            return True
        except:
            self._conn.rollback()
            return False

    def store_result(self):
        """
        Transfers a result set from a prepared statement
        :rtype: bool
        """
        try:
            self._store_result = True
            return True
        except:
            return False

    def fetch(self):
        """
        Fetch results from a prepared statement into the bound variables
        NOTE: results will be fetched as a list so always use [0] to print
        the result. e.g: print(list1[0])
        :rtype: bool
        """
        try:
            if self._store_result and self.num_rows > 0:
                for row in range(self._temp_index, self.num_rows):
                    _row = self._fetched_rows[row]
                    for col in range(0, len(_row)):
                        if len(self._bind_args[col]) != 0:
                            del self._bind_args[col][0]
                        (self._bind_args[col]).append(_row[col])
                    self._temp_index = row+1
                    return True
            return False
        except:
            return False

    def free_result(self):
        """
        Frees stored result memory for the given statement handle
        :rtype: bool
        """
        try:
            self.num_rows = 0
            self.affected_rows = 0
            self._store_result = True
            self._fetched_rows = list()
            self._temp_index = 0
            self._bind_args = tuple()
            return True
        except:
            return False

    def close(self):
        """
        Closes a prepared statement
        :rtype: bool
        """
        try:
            del self._conn
            del self._query
            self.num_rows = 0
            self.affected_rows = 0
            self._params = tuple()
            self._store_result = False
            self._fetched_rows = list()
            self._temp_index = 0
            self._bind_args = tuple()
            return True
        except:
            return False
