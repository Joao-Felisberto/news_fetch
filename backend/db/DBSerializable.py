from abc import ABC, abstractmethod


class DBSerializable(ABC):
    """
    This class handles the storage and serialization of objects to be stored in a sqlite database.
    Contains methods to get the data from a db and to store them in a db.
    Subclasses must implement the methods.
    """

    def __init__(self, primary_key, table, db_manager):
        """
        Instantiates an object that is stored in a database
        :param primary_key: the name of the primary key's field on the table
        :param table: the table where it is stored
        :param db_manager: the DBManager that is connected to the db. Used to run the queries
        """
        self.__table = table
        self.__db_manager = db_manager
        self.__primary_key = primary_key
        self.__attributes_map = {}
        # self.__attributes_map = attributes_map

        # if self.__db_manager.get_by_id(self) is not None:
        #     for k in attributes_map:
        #         if attributes_map[k] is None:
        #             attributes_map[k] = self.__db_manager.get_attr(k, self)
        #
        #     self.__attributes_map = attributes_map

    def to_db(self):
        """
        Serializes the object and sends it to the database if it is valid
        """
        # try:
        #     self.__db_manager.store(self)
        # except OperationalError:
        #     print("Not a valid object")
        self.__db_manager.store(self)

    @abstractmethod
    def save_attr_map(self):
        """
        This method should be implemented to save all relevant object data to it's attribute map
        """
        pass

    @abstractmethod
    def load_attr_map(self):
        """
        This method should be implemented to load all relevant object data from it's attribute map
        """
        pass

    def set_attr_map(self, attr_map):
        """
        This method is used to initialize an object from it's ID
        :param attr_map: The attributes to initialize the object
        """
        # pass
        self.__attributes_map = attr_map
        # self.to_db()

    def set_attr(self, attr, new_val):
        """
        A method to be used in setters to update the data in the db
        :param attr: the db atribute name
        :param new_val: the new value to be assigned
        """
        self.__attributes_map[attr] = new_val
        self.to_db()

    def link_to(self, db_serializable, f_k):
        """
        Sends the primary key of this object to the db_serializable's attribute
        :param f_k: The foreign key to be linked with this object
        :param db_serializable: The object which has a foreign key on this object's table
        """
        db_serializable.set_attr(f_k, self.__attributes_map[self.__primary_key])

    def get_attr(self, attr):
        return self.__attributes_map[attr]

    def get_table(self):
        return self.__table

    def get_db_man(self):
        return self.__db_manager

    def get_primary_key(self):
        """
        :return: a tuple (primary key, primary key's value)
        """
        # print(self.__attributes_map)
        return self.__primary_key, self.__attributes_map[self.__primary_key]

    def get_attributes_map(self):
        return self.__attributes_map
