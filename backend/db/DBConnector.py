import sqlite3 as sql


class _DBConnector:
    """
    A class to handle database low level actions, like connections and query execution
    """

    def __init__(self, db):
        """
        Connects to the database
        :param db: the database
        """
        self.__name = db
        self.__db = sql.connect(db)

    def _run(self, query):
        """
        Executes a query and returns it's result
        :param query: the query to be executed
        :return: the result for the query
        """
        q = self.__db.cursor().execute(query)
        res = q.fetchall()
        self.__db.commit()
        return res

    def __del__(self):
        """
        Closes the database connection when the object gets destructed
        """
        try:
            self.__db.close()
        except AttributeError:
            pass

    def _get_db(self):
        return self.__name
