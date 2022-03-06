import matplotlib.pyplot as plt

from db.DBManager import DBManager


# from matplotlib import interactive
# interactive(True)

def plot_articles_per_day():
    """
    Shows how many articles were posted for every day of the year
    """
    db = DBManager("/home/me/PycharmProjects/news/backend/db/db/db.db")
    times = db.get_times_between('2021-08-08', '2021-08-14')

    print(times)

    ydays = [t.timetuple().tm_yday for t in times]
    x = list(range(ydays[0], ydays[-1] + 1))
    print(x)
    y = [len([d for d in ydays if d == n]) for n in x]

    plt.scatter(x, y)
    plt.show()


def plot_articles_by_interval():
    """
    Shows how many articles were posted by hour
    """
    db = DBManager("/home/me/PycharmProjects/news/backend/db/db/db.db")
    # times = db.get_times_between('2021-08-08', '2021-08-14')
    times = db.get_times_between()

    minutes = [t.hour + t.minute / 60 for t in times]
    x = list(set(minutes))
    # print(x)
    y = [len([m for m in minutes if m == n]) for n in x]

    print(len(x))
    print(len(y))

    plt.scatter(x, y)
    plt.show()


if __name__ == '__main__':
    # plot_articles_per_day()
    plot_articles_by_interval()
