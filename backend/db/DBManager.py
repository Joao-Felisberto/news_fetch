from datetime import datetime
from sqlite3 import IntegrityError

from db.DBConnector import _DBConnector
# TODO: prevent SQL injection https://realpython.com/prevent-python-sql-injection/
#   As if a backend website would create articles named "; drop database backend; --"...
from db.objects.article_header import ArticleHeader


class DBManager(_DBConnector):
    """
    A class to normalize all queries to the database
    """

    def __init__(self, db):
        _DBConnector.__init__(self, db)

    @staticmethod
    def __to_update_query(attributes_map):  # Pode dar para simplificar esta aproximação
        """
        Parses a map {<db_attr> : <db_val>} into UPDATE sql syntax
        :param attributes_map: the map {<db_attr> : <db:val>}
        :return: a formatted sql string
        """
        query = ""
        #  attributes_map: {<db_key> : <db_new_val>}

        for k in attributes_map:
            query += ("{} = '{}', ".format(k, attributes_map[k]) if attributes_map[k] != 'DEFAULT' else
                      "{} = {}, ".format(k, attributes_map[k]))

        query = query[:-2]
        return query

    @staticmethod
    def __to_insert_query(attributes_map):  # Pode dar para simplificar esta aproximação
        """
        Parses a map {<db_attr> : <db_val>} into INSERT INTO sql syntax
        :param attributes_map: the map {<db_attr> : <db:val>}
        :return: a formatted sql string
        """
        query = "("
        #  attributes_map: {<db_key> : <db_new_val>}

        for k in attributes_map:
            query += ("'{}', ".format(attributes_map[k]) if attributes_map[k] != 'DEFAULT' else
                      "{}, ".format(attributes_map[k]))

        query = query[:-2] + ")"
        return query

    def store(self, db_serializable):
        """
        Strores a db_serializable in the db
        :param db_serializable: the object we want to store in the db
        """
        table = db_serializable.get_table()
        primary_key = db_serializable.get_primary_key()[0]
        obj_id = db_serializable.get_attributes_map()[primary_key]
        new_obj_data = db_serializable.get_attributes_map()

        if new_obj_data[primary_key] is not None:
            try:
                print(f"INSERT INTO {table} VALUES {self.__to_insert_query(new_obj_data)}")
                self._run(f"INSERT INTO {table} VALUES {self.__to_insert_query(new_obj_data)}")
            except IntegrityError:
                self._run(f"UPDATE {table} SET {self.__to_update_query(new_obj_data)} WHERE {primary_key} = '{obj_id}'")

    def delete(self, db_serializable):
        """
        Removes a db_serializable from the db
        :param db_serializable: the object we want to remove from the db
        """

        table = db_serializable.get_table()
        primary_key = db_serializable.get_primary_key()[0]
        obj_id = db_serializable.get_attributes_map()[primary_key]
        new_obj_data = db_serializable.get_attributes_map()

        if new_obj_data[primary_key] is not None:
            self._run(f"DELETE FROM {table} WHERE {primary_key} = '{obj_id}'")

    def get_table_size(self, table):
        return len(self._run(f"SELECT * FROM {table}"))

    def create(self):
        self._run("CREATE TABLE IF NOT EXISTS article_headers (post_date smalldatetime, title text, link text)")

    def get_header_by_id(self, index=None, start=0, end=None):
        header = self._run(f"SELECT * FROM article_headers ORDER BY post_date DESC")

        print(f"!!!\t[{start}:{end}]: {str(len(header))}")
        if index is not None:
            h = header[index]
            return ArticleHeader(self, datetime.strptime(h[0], "%Y-%m-%d %H:%M:%S"), h[1], h[2])
        elif end is not None:
            header = header[start:end]
        else:
            header = header[start:]

        res = []
        for h in header:
            res.append(ArticleHeader(self, datetime.strptime(h[0], "%Y-%m-%d %H:%M:%S"), h[1], h[2]))

        return res

    def reset_test_db(self):
        # print(self._get_db()[-10:])
        if self._get_db()[-10:] == "test_db.db":
            self._run("DELETE FROM article_headers")

    def get_times_between(self, start=None, end=None):
        if start is None and end is None:
            strs = self._run(
                f"SELECT post_date FROM main.article_headers ORDER BY post_date")
        else:
            strs = self._run(
                f"SELECT post_date FROM main.article_headers WHERE post_date BETWEEN '{start}' AND '{end}' ORDER BY post_date")

        return [datetime.strptime(t[0], "%Y-%m-%d %H:%M:%S") for t in strs]
