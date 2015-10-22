#!/usr/bin/python3
import sys

__title__ = 'SQLiteException'
__version__ = '0.2.0'
__author__ = 'Muntashir Al-Islam'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2015 Muntashir Al-Islam'

"""
    The SQLiteException class

    date: 21/10/2015
"""


class SQLiteException:
    """
     Represents a SQLite Exception.

     Note: SQLite is not as smart as MySQLi.
     So things like error code and sqlstate is not available in SQLite.
     I did not use the sqlstate but errno in my code.
     But errno does not return any code rather it returns
     an exception class if any error occurs.
     Also, currently error_list doesn't return the error list of the last command
     but all the errors from the beginning

     Notice: There's a mysql_warning class in PHP which I think do not necessary at all
     since there is no proper way to show sql related warning in SQLite.
     SQLiteException serves the purpose of mysql_sql_exception class.
    """
    error = ""           # Returns a string description of the last error
    errno = ""           # Returns the error code (actually error type class) for the most recent function call
    error_list = list()  # Returns a list of errors from the last command executed TODO: more development needed

    def _handle_error(self):
        """
        Handles error
        :rtype: None
        """
        e = sys.exc_info()
        self.errno = e[0]
        self.error = e[1]
        self.error_list.append([self.errno, self.error])
        # If you want to raise an error, just uncomment the line below
        # This may create two exception instead of one
        # raise e[0](e[1])
