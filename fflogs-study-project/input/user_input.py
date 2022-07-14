"""Manages user inputs to get links to log files."""

from collections import namedtuple
import re


def user_input() -> namedtuple:
    """"""
    text = """
Input '1-5' to analyze one of the log-sets previously defined.
(3 is an invalid comp, the rest is valid!)

Input full log url to add to the list of logs to be summarized.

Input parameter to change:
    'show': Show scraping process (sets headless=False)
    'hide': Hide scraping process (sets headless=True, baseline)
    'kills': Summarize only kills in given logs (sets type='kills')
    'wipes': Summarize only wipes in given logs (sets type='wipes')
    'all': Summarize both kills and wipes in given logs (baseline)
    'debug': Start the dash app in debug mode

Input 'config' to show current configuration.
Input 'y' to start the process, 'q' to abort.
    """
    print(text)

    FullInput = namedtuple("FullInput", ["logs", "headless", "type", "debug"])
    logs = []
    type = "all"
    headless = True
    debug = False

    while True:
        user_input = input("Input: ")

        # match-case, introduced in python 3.10
        match user_input:
            case "1" | "2" | "3" | "4" | "5":
                logs = predef_links(int(user_input))
                print(f"Set links to predefined logs {user_input}.")
            case "kills" | "wipes" | "all":
                print(f"Set type to {user_input}.")
                type = user_input
            case "show":
                print("Scraping will be shown.")
                headless = False
            case "hide":
                print("Scraping will not be shown.")
                headless = True
            case "debug":
                print("Dash debug mode set.")
                debug = True
            case "config":
                print(FullInput(logs, headless, type, debug))
            case "y":
                print("Confirmed.")
                break
            case "q":
                exit()
            case _:
                if len(user_input) > 10:
                    print("Checking url...")
                    print(user_input)
                    if check_url(user_input):
                        print("Link has been added.")
                        logs.append(user_input)
                    else:
                        print("The log seems to be invalid.")
                print("This does not seem to be a valid input.")

    full_input = FullInput(logs, headless, type, debug)
    print("Processing...")
    return full_input


def user_input2() -> namedtuple:
    """"""
    text = """
Input '1-5' to analyze one of the log-sets previously defined.
(3 is an invalid comp, the rest is valid!)

Input full log url to add to the list of logs to be summarized.

Input parameter to change:
    'show': Show scraping process (sets headless=False)
    'hide': Hide scraping process (sets headless=True, baseline)
    'kills': Summarize only kills in given logs (sets type='kills')
    'wipes': Summarize only wipes in given logs (sets type='wipes')
    'all': Summarize both kills and wipes in given logs (baseline)
    'debug': Start the dash app in debug mode

Input 'y' to start the process, 'q' to abort.
    """
    print(text)

    FullInput = namedtuple("FullInput", ["logs", "headless", "type", "debug"])
    logs = []
    type = "all"
    headless = True
    debug = False

    while True:
        user_input = input("Input: ")

        if user_input == ("kills" or "wipes" or "all"):
            print(f"Set type to {user_input}.")
            type = user_input
        elif user_input == "show":
            print("Scraping will be shown.")
            headless = False
        elif user_input == "hide":
            print("Scraping will not be shown.")
            headless = False
        elif user_input == "debug":
            print("Dash debug mode set.")
            debug = True
        elif len(user_input) > 40:
            print("Checking url...")
            print(user_input)
            if check_url(user_input):
                print("Link has been added.")
                logs.append(user_input)
            else:
                print("The log seems to be invalid.")
        elif user_input == "y":
            print("Confirmed.")
            break
        elif user_input == "q":
            exit()
        else:
            try:
                logs = predef_links(int(user_input))
                print(f"Set links to predefined logs {user_input}.")
            except IndexError:
                print("Please choose a valid number (1-5).")
            except ValueError:
                print("This does not seem to be a valid input.")

    full_input = FullInput(logs, headless, type, debug)
    print("Processing...")
    return full_input


def check_url(url: str) -> bool:
    """Check url for valid log, return True if valid."""
    regex = r"https:\/\/www.fflogs.com\/reports\/(a:)?[a-zA-Z0-9]{16}(\/*)?"
    return re.match(regex, url)


def predef_links(num: int) -> list[str]:
    """Predefined links for testing purposes.

    Returns: list, where each element is a link.
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
