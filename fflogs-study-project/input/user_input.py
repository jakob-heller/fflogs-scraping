"""Manages user inputs to get links to log files."""


def user_input(num: int) -> list[str]:
    """Asks for direct links or log specific code.

    Returns: list, where each element is either a complete link or the log
    specific code.
    """
    # 1 log, kills
    links1 = ["https://www.fflogs.com/reports/LnjBh2tfZRyv8rpD"]

    # 2 logs, kills, valid comp
    links2 = ["https://www.fflogs.com/reports/LnjBh2tfZRyv8rpD",
              "https://www.fflogs.com/reports/hacvwXKb8mFYrAdx"]

    # 3 logs, kills, invalid comp
    links3 = ["https://www.fflogs.com/reports/LnjBh2tfZRyv8rpD",
              "https://www.fflogs.com/reports/hacvwXKb8mFYrAdx",
              "https://www.fflogs.com/reports/vbMftnwLWzHK2prZ"]

    # 2 logs, wipes, valid comp
    links4 = ["https://www.fflogs.com/reports/waNVQPnycRWmf3r8",
              "https://www.fflogs.com/reports/Qxdy8D9tKMcLkRvq"]

    # 8 logs, wipes, valid comp
    links5 = ["https://www.fflogs.com/reports/waNVQPnycRWmf3r8",
              "https://www.fflogs.com/reports/Qxdy8D9tKMcLkRvq",
              "https://www.fflogs.com/reports/vDYT6KryG8QHkpfd",
              "https://www.fflogs.com/reports/qYCQyH1fhc8TgJXZ",
              "https://www.fflogs.com/reports/ZKVArHm4GNPJTgD9",
              "https://www.fflogs.com/reports/BnKVdNY9M7CgRDfX",
              "https://www.fflogs.com/reports/Wm6THJ1VXDBRvpfQ",
              "https://www.fflogs.com/reports/f4QzaWYpkr7wLJnv"]

    links = (links1, links2, links3, links4, links5)

    return links[num-1]
