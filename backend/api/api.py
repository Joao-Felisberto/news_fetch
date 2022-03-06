# https://rapidapi.com/blog/how-to-build-an-api-in-python/
import os

from flask import Flask, request
from flask_restful import Api

from db.DBManager import DBManager

app = Flask(__name__)
api = Api(app)


@app.route("/news/latest/<int:index>")
def latest(index=0):
    print(f"api.py: {os.getcwd()}")
    __db_man = DBManager("backend/db/db/db.db")
    header = __db_man.get_header_by_id(index=index).get_attributes_map()
    header["post_date"] = header["post_date"].strftime("%Y-%m-%d %H:%M:%S")
    print(header)
    return str(header), 200


@app.route("/news/")
def interval():
    __db_man = DBManager("backend/db/db/db.db")

    start = request.args.get('start')
    end = request.args.get('end')

    header = __db_man.get_header_by_id(
        start=0 if start is None else int(start),
        end=10 if end is None else int(end)
    )

    # print(f"!!!\t{int(start)}:{int(end)}")

    header = [h.get_attributes_map() for h in header]

    for h in header:
        h["post_date"] = h["post_date"].strftime("%Y-%m-%d %H:%M:%S")

    return str(header), 200


@app.route('/site/style.css')
def styles():
    with open('site/style.css') as style:
        return style.read()


@app.route('/site/')
def interval_site():
    __db_man = DBManager("backend/db/db/db.db")

    start = request.args.get('start')
    end = request.args.get('end')

    header = __db_man.get_header_by_id(
        start=0 if start is None else int(start),
        end=10 if end is None else int(end)
    )

    header = [h.get_attributes_map() for h in header]

    for h in header:
        h["post_date"] = h["post_date"].strftime("%Y-%m-%d %H:%M:%S")

    with open("site/news_list.html") as site:
        res = site.read()

        table = ''.join([
            f'<tr><td>{h["post_date"]}</td><td>{h["title"]}</td><td><a href=\"{h["link"]}\">original</a></td></tr>'
            for h in header])

        res = res.format(table)

        return res, 200


# class Latest(Resource):
#
#     def __init__(self):
#         self.__db_man = DBManager("tests/test_db.db")
#
#     def get(self, index=1):
#         print(f"api.py: {os.getcwd()}")
#         header = self.__db_man.get_header_by_id(index).get_attributes_map()
#         header["post_date"] = header["post_date"].strftime("%Y-%m-%d %H:%M:%S")
#         print(header)
#         return header, 200


if __name__ == '__main__':
    # api.add_resource(Latest, "/latest/")
    app.run(debug=True)
