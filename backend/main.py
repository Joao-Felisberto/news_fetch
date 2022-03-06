import os
from sys import argv

from api.api import app
from db.DBManager import DBManager
from db.objects.article_header import ArticleHeader
from plugins import plugin_loader as pll

if __name__ == '__main__':
    print(f"main.py: {os.getcwd()}")
    cmd = argv[1]

    if cmd == "--fetch" or cmd == "-f":
        succ, fail = pll.get_plugins()

        for v in succ:
            print("Successfully imported " + v.__name__)

        if len(fail) != 0:
            print("ERROR ===========================\\\\")
            for v in fail:
                print("Failed to import " + v.__name__ + ": " + str(fail[v]))
            print("ERROR ===========================//")

        db = DBManager("backend/db/db/db.db")
        db.create()
        for v in succ:

            news = v.fetch_news()

            for art in news:
                # Some weird bug with `publico` that makes an empty article wit length 1
                if len(art) != 3:
                    continue

                a = ArticleHeader(db, art[2], art[0], art[1])
                a.to_db()

    elif cmd == "--read" or cmd == "-r":
        if len(argv) < 3:
            print("Not enough arguments, please tell the article you want to see")
            exit(1)

    elif cmd == "--api" or cmd == "-a":
        # api.add_resource(Latest, "/latest/")
        app.run(debug=False, host='0.0.0.0', port=80)
