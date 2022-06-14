import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Scraping:

    def __init__(self, logs: list, browser: str = "Firefox"):
        self.logs = logs
        self.comp = ()

        if browser == "Firefox":
            self.driver = webdriver.Firefox()
        elif browser == "PhantomJS":
            self.driver = webdriver.PhantomJS()

    def to_summary(self) -> None:
        self.driver.get(self.logs[0])

        popup_xp = "/html/body/div[2]/div/div/div/div[2]/div/button[1]"
        self.driver.find_element(By.XPATH, popup_xp).send_keys(Keys.ENTER)

        all_enc_xp = "/html/body/div[4]/div[2]/div[5]/div/div/div/div[2]/div/a[3]"
        self.driver.find_element(By.XPATH, all_enc_xp).click()

        time.sleep(3)

    def get_comp(self) -> str:
        parsed_summary = BeautifulSoup(self.driver.page_source, "html.parser")
        comp_str = parsed_summary.find_all(class_="composition-entry")

        return str(comp_str)

    def quit(self):
        self.driver.quit()

    def build_composition(self, comb_html: str) -> tuple[str]:
        """Parse html string with regex and build up group composition as tuple.

        Args:
          comb_html: html string of the composition table.

        Returns:
          8-tuple of strings, containing jobs of all 8 players.
        """
        composition = list(re.findall("\"[a-zA-Z]*\"", comb_html))
        composition = [s.strip('"') for s in composition]

        self.comp = composition

        return tuple(composition)


logs = list(("https://www.fflogs.com/reports/VwfG79rj4dF3gLqK",
            "https://www.fflogs.com/reports/VwfG79rj4dF3gLqK"))
soup = Scraping(logs, "Firefox")
soup.to_summary()
soup.build_composition(soup.get_comp())
soup.quit()
print(soup.comp)
