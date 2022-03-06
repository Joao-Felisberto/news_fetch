import importlib
import os

# https://docs.python.org/3/library/inspect.html allows for method inspection, insights on method signature
# import inspect

PLUGINS = "backend/plugins/scrappers/"

REQUIRED = ("fetch_news", "fetch_article")


def get_plugins():
    """
    Fetches all valid plugins
    This will test all .py files and only return the ones with a valid plugin structure
    (if they contain all required methods)
    :return: A list with all valid plugins and a dict with all failed plugins and the reason for their failure
    """

    possible = __get_names()
    valid = []
    failed = {}

    for pl in possible:
        pl = importlib.import_module('.', pl[:-3].replace('/', '.'))

        passed = True
        for foo in REQUIRED:
            if foo not in dir(pl):
                try:
                    failed[pl].append("Missing method: " + foo)
                except KeyError:
                    failed[pl] = ["Missing method: " + foo]

                passed = False
                continue

        if passed:
            valid.append(pl)

    return valid, failed


def __get_names():
    """
    Fetches all .py files inside the plugins' directory
    :return: A list with all .py files inside the plugins' directory
    """
    # The directory where all plugins can be found
    pl_names = os.listdir(PLUGINS)

    return [PLUGINS[7:] + pl for pl in pl_names if pl.endswith('.py') and not pl.startswith("_")]


if __name__ == '__main__':
    succ, fail = get_plugins()

    for v in succ:
        print("Scessfully imported " + v.__name__)

    if len(fail) != 0:
        print("===========================")

    for v in fail:
        print("Failed to import " + v.__name__ + ": " + str(fail[v]))

    if len(fail) != 0:
        print("===========================")

    for v in succ:
        news = v.fetch_news()

        art = news[0]
        print(v.fetch_article(art[1]))
