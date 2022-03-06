# from api.Serializable import Serializable
from db.DBSerializable import DBSerializable


class ArticleHeader(DBSerializable):
    def __init__(self, db_manager, post_date, title, link):
        super().__init__("post_date", "article_headers", db_manager)
        self.__post_date = post_date
        self.__title = title.replace('\'', '')
        self.__link = link

        self.save_attr_map()

    def save_attr_map(self):
        self.set_attr_map({"post_date": self.__post_date, "title": self.__title, "link": self.__link})

    def load_attr_map(self):
        self.__post_date = self.get_attr("post_date")
        self.__title = self.get_attr("title")
        self.__link = self.get_attr("link")

    def __eq__(self, other):
        return self.__post_date == other.__post_date and \
               self.__title == other.__title and \
               self.__link == other.__link
