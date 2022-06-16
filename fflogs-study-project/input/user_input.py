"""Manages user inputs to get links to log files."""


def user_input() -> list[str]:
    """Asks for direct links or log specific code.

    Returns: list, where each element is either a complete link or the log
    specific code.
    """
    # 1 log, kills
    links1 = ["https://www.fflogs.com/reports/a:VrNFghvTcL3J48WK"]

    # 2 logs, kills, valid comp
    links2 = ["https://www.fflogs.com/reports/a:Byj6V2YK3NnvaJQH",
              "https://www.fflogs.com/reports/a:rVZpJMB7cLt6xWHm"]

    # 3 logs, kills, invalid comp
    links3 = ["https://www.fflogs.com/reports/a:Byj6V2YK3NnvaJQH",
              "https://www.fflogs.com/reports/a:rVZpJMB7cLt6xWHm",
              "https://www.fflogs.com/reports/a:VrNFghvTcL3J48WK"]

    # 2 logs, wipes, valid comp
    links4 = ["https://www.fflogs.com/reports/a:Q8ChqfGPrVNKDjYb",
              "https://www.fflogs.com/reports/a:hJxtKzVgXTN3rkaq"]

    # 8 logs, wipes, valid comp
    links5 = ["https://www.fflogs.com/reports/a:Q8ChqfGPrVNKDjYb",
              "https://www.fflogs.com/reports/a:hJxtKzVgXTN3rkaq",
              "https://www.fflogs.com/reports/a:H7rqJ6yX9x3vmaYk",
              "https://www.fflogs.com/reports/a:HVWDad7PgZ9AzbR8",
              "https://www.fflogs.com/reports/a:HVWDad7PgZ9AzbR8",
              "https://www.fflogs.com/reports/a:6MjdTy4fAvkC9hz1",
              "https://www.fflogs.com/reports/a:A7rQDhcTgR68GJf2",
              "https://www.fflogs.com/reports/a:tPhgqTCNVcFLG6vx"]

    return links5
