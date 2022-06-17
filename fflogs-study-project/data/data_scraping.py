"""Includes implementation of Scraping class."""

import time
import os
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraping:
    """Implementation of all necessary scraping methods.

    Attributes:
      logs: list of logs (links) to be scraped.
      enc_type: int indicating what encounters should be taken into account.
      driver: Firefox webdriver object.

      comp: 8-tuple of job-composition in logs.
    """

    def __init__(self, logs: list, encounters_type: str, headless=True, adblock=True):
        """Initialize object with given attributes, start driver.

        Args:
          logs: list of log links (user input)
          encounters_type: include either wipes, kills or all encounters.
          headless: True if browser should be invisible, false if visible.
        """
        self.logs = logs
        self.comp = ()

        if encounters_type == "wipes":
            self.enc_type = 0
        elif encounters_type == "kills":
            self.enc_type = 1
        elif encounters_type == "all":
            self.enc_type = 2
        else:
            raise AttributeError("Select a valid encounter type.")

        options = webdriver.FirefoxOptions()
        if headless:
            options.headless = True

        # Set profile to either profile including ublock or default
        if adblock:
            ffprofile = webdriver.FirefoxProfile("firefox profile with adblock")
        else:
            ffprofile = webdriver.FirefoxProfile()

        # Get relative path to folder for saving csv files
        dirname = os.path.dirname(__file__)
        csv_path = os.path.join(dirname, "csv")

        # Delete previous csv files
        for filename in os.listdir(csv_path):
            file_path = os.path.join(csv_path, filename)
            os.unlink(file_path)

        # Adjust profile to automatically download csv files to specified path
        ffprofile.set_preference("browser.download.folderList", 2)
        ffprofile.set_preference("browser.download.manager.showWhenStarting", False)
        ffprofile.set_preference("browser.download.dir", csv_path)
        ffprofile.set_preference("browser.helperApps.neverAsk.saveToDisk", "csv")

        # Start Firefox driver with options (headless or not) and profile
        self.driver = webdriver.Firefox(ffprofile, options=options)

    def quit(self):
        """Close browser/ quit driver."""
        self.driver.quit()

    def wait_until(self, xpath: str, timeout: int = 10, type: str = "present"):
        """Wait till specified element is loaded (or timeout) and return it."""
        if type == "clickable":
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath)))
        elif type == "present":
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

    def first_popups(self):
        """Need to accept pop-up when visiting fflogs for the first time."""
        self.driver.get("https://www.fflogs.com/")

        popup_xp = "//button/span[./text()='AGREE']"
        self.wait_until(popup_xp, type="clickable").click()

        cookies = "//div[@class='cc-compliance']"
        self.wait_until(cookies, type="clickable").click()

    def to_summary(self, log_num: int = 0) -> None:
        """Open log link from list and navigate to all encounters summary."""
        self.driver.get(self.logs[log_num])

        fights_xp = ("//div[@class='report-overview-boss-pulls ']/a[contains(., 'All Wipes')]",  # noqa: E501
                     "//div[@class='report-overview-boss-pulls ']/a[contains(., 'All Kills')]",  # noqa: E501
                     "//div[@class='report-overview-boss-pulls ']/a[contains(., 'All Encounters')]")  # noqa: E501

        self.wait_until(fights_xp[self.enc_type], type="clickable").click()

    def get_comp(self) -> str:
        """Get html of summary page an return the composition table."""
        self.wait_until("//table[@class='composition-table']", type="present")

        parsed_summary = BeautifulSoup(self.driver.page_source, "html.parser")
        comp_html = parsed_summary.find_all(class_="composition-entry")

        return str(comp_html)

    def check_comp(self, comp_html: str) -> tuple[str]:
        """Parse html string with regex and check/ update group composition.

        Args:
          comb_html: html string of the composition table.

        Raises:
          AttributeError: if comp is different to already existing comp.
        """
        comp = list(re.findall("\"[a-zA-Z]*\"", comp_html))
        comp = [s.strip('"') for s in comp]

        if len(self.comp) > 0 and sorted(self.comp) != sorted(tuple(comp)):
            self.quit()
            raise AttributeError(("Group comps in provided logs don't match."))
        else:
            self.comp = tuple(comp)

    def to_damage_dealt(self) -> None:
        """Navigate from "summary" to "damage dealt" tab."""
        sum_url = self.driver.current_url
        dd_url = (sum_url + "&type=damage-done")

        self.driver.get(dd_url)

    def get_damage_dealt(self) -> None:  # TODO
        """Download csv from damage tab."""
        dd_csv_xp = "//button/span[./text()='CSV']"
        self.wait_until(dd_csv_xp, type="clickable").click()

    def to_healing_done(self) -> None:
        """Navigate from "damage dealt" to "healing" tab."""
        dd_url = self.driver.current_url
        hd_url = dd_url.replace("&type=damage-done", "&type=healing")

        self.driver.get(hd_url)

    def get_healing_done(self) -> None:  # TODO
        """Download csv from healing tab."""
        time.sleep(0.4)

        hd_csv_xp = "//button/span[./text()='CSV']"
        self.wait_until(hd_csv_xp, type="clickable").click()

    def parse_logs(self) -> None:
        """Parse and scrape all given logs."""
        self.first_popups()
        for log in range(len(self.logs)):
            self.to_summary(log)
            self.check_comp(self.get_comp())
            self.to_damage_dealt()
            self.get_damage_dealt()
            self.to_healing_done()
            self.get_healing_done()
        self.quit()
