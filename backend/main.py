import json
import os
from datetime import datetime
from sys import argv

from discord import HTTPException

from api.api import app
from db.DBManager import DBManager
from db.objects.article_header import ArticleHeader
from plugins import plugin_loader as pll


def fetch(db: DBManager) -> list[ArticleHeader]:
    # global db
    succ, fail = pll.get_plugins()
    for v in succ:
        print("Successfully imported " + v.__name__)
    if len(fail) != 0:
        print("ERROR ===========================\\\\")
        for v in fail:
            print("Failed to import " + v.__name__ + ": " + str(fail[v]))
        print("ERROR ===========================//")
    # db = DBManager("backend/db/db/db.db")
    # db.create()

    articles = []
    for v in succ:

        news = v.fetch_news()

        for art in news:
            # Some weird bug with `publico` that makes an empty article wit length 1
            if len(art) != 3:
                continue

            a = ArticleHeader(db, art[2], art[0], art[1])
            a.to_db()
            articles.append(a)

    return articles


if __name__ == '__main__':
    print(f"main.py: {os.getcwd()}")
    cmd = argv[1]

    if cmd == "--fetch" or cmd == "-f":
        db = DBManager("backend/db/db/db.db")
        db.create()

        fetch(db)

    elif cmd == "--read" or cmd == "-r":
        if len(argv) < 3:
            print("Not enough arguments, please tell the article you want to see")
            exit(1)

    elif cmd == "--api" or cmd == "-a":
        # api.add_resource(Latest, "/latest/")
        app.run(debug=False, host='0.0.0.0', port=80)

    elif cmd == "--bot" or cmd == "-b":
        import discord
        from time import sleep

        with open("bot_config.json", 'r') as f:
            cfg = json.loads(f.read())

        channel = cfg["news_channel"]

        with open("token", 'r') as f:
            token = f.read()

        print("loaded cfg")

        client = discord.Client()


        @client.event
        async def on_ready():
            print("Client launched")

            db = DBManager("backend/db.db")
            db.create()

            print("db connected")

            # def idfk(msg):
            #     print("SEND", msg)
            #     await client.get_channel(int(channel)).send(msg)

            delay = 5 * 60
            while 1:
                print("Iteration")
                last_date = db.get_last_article_time()

                print("last date:", last_date.strftime('%Y-%m-%d %H:%M:%S'))

                arts = [a for a in fetch(db) if a.get_time() > last_date]

                print(last_date, len(arts), [a.get_attributes_map() for a in arts])

                for a in arts:
                    msg = a.get_attributes_map()
                    date_: datetime = msg['post_date']
                    # msg = f"[{date_.strftime('%Y-%m-%d %H:%M:%S')}]: **{msg['title']}**: <{msg['link']}>"
                    # print(msg)
                    # asyncio.create_task(client.get_channel(int(channel)).send(msg))
                    # _thread.start_new_thread(idfk, (msg, ))

                    embed = discord.Embed(
                        title=msg['title'],
                        url=msg['link'],
                        timestamp=date_  # .strftime('%Y-%m-%d %H:%M:%S')
                    )

                    embed.add_field(name="Introdução", value="//TODO", inline=False)

                    # await client.get_channel(int(channel)).send(msg)
                    try:
                        await client.get_channel(int(channel)).send(embed=embed)
                    except HTTPException:
                        embed = discord.Embed(
                            title=msg['title'],
                            timestamp=date_  # .strftime('%Y-%m-%d %H:%M:%S')
                        )
                        await client.get_channel(int(channel)).send(embed=embed)

                sleep(delay)


        client.run(token)
