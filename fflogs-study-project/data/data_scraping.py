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
      logs: list of logs (urls) to be scraped.
      enc_type: indicates what encounters should be taken into account.
      driver: Firefox webdriver object.
      cookies: bool, True if cookies should be accepted.
      comp: 8-tuple of job-composition in logs.
    """

    def __init__(self, logs, type="all", headless=True, cookies=False):
        """Initialize object with given attributes, start driver.

        Args:
          logs: list of log links (user input)
          encounters_type: str, include either wipes, kills or all encounters.
          headless: bool, True if browser should be invisible.
          cookies: bool, True if cookies should be accepted.
        """
        self.logs = logs
        self.comp = ()
        self.cookies = cookies

        if type == "wipes" or "kills" or "all":
            self.enc_type = type
        else:
            raise AttributeError("Select a valid encounter type.")

        options = webdriver.FirefoxOptions()
        if headless:
            options.headless = True

        # Get relative path to csv folder
        dirname = os.path.dirname(__file__)
        csv_path = os.path.join(dirname, "csv")

        # Delete previous csv files
        for filename in os.listdir(csv_path):
            file_path = os.path.join(csv_path, filename)
            os.unlink(file_path)

        # Create FirefoxProfile and adjust download preferences
        ffprofile = webdriver.FirefoxProfile()
        ffprofile.set_preference("browser.download.folderList", 2)
        ffprofile.set_preference("browser.download.manager.showWhenStarting", False)
        ffprofile.set_preference("browser.download.dir", csv_path)
        ffprofile.set_preference("browser.helperApps.neverAsk.saveToDisk", "csv")

        # Start Firefox driver with options (headless or not) and profile
        self.driver = webdriver.Firefox(ffprofile, options=options,
                                        executable_path="geckodriver.exe")

        # Install and activate ublock origin (adblock) from xpi
        self.driver.install_addon("ublock_origin-1.43.0.xpi", temporary=True)
        ffprofile.add_extension(extension="ublock_origin-1.43.0.xpi")

    def parse_logs(self) -> None:
        """Parse and scrape all given logs."""
        if self.cookies:
            self.accept_cookies()
        for log in self.logs:
            self.to_summary(log)
            self.check_comp(self.get_comp())
            self.to_damage_dealt()
            self.get_damage_dealt()
            self.to_healing_done()
            self.get_healing_done()
        self.quit()

    def quit(self) -> None:
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

    def accept_cookies(self) -> None:
        """Accept cookies."""
        self.driver.get("https://www.fflogs.com/")
        cookies = "//div[@class='cc-compliance']"
        self.wait_until(cookies, type="clickable").click()

    def to_summary(self, log_url: str) -> None:
        """Modify url and open summary page."""
        url = (log_url + "#boss=-2")

        if self.enc_type == "wipes":
            url = (url + "&wipes=1")
        elif self.enc_type == "kills":
            url = (url + "&wipes=2")
        # "All" encounters is baseline, no need to add anything for that case.
        self.driver.get(url)

    def get_comp(self) -> str:
        """Get html of summary page an return the composition table."""
        self.wait_until("//table[@class='composition-table']", type="present")

        parsed_summary = BeautifulSoup(self.driver.page_source, "html.parser")
        comp_html = parsed_summary.find_all(class_="composition-entry")

        return str(comp_html)

    def check_comp(self, comp_html: str) -> None:
        """Parse html string with regex and check group composition."""
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

        # Scroll down so the cookies don't obscure the field we want to click
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def get_damage_dealt(self) -> None:  # TODO
        """Download csv from damage tab."""
        dd_csv_xp = "//button/span[./text()='CSV']"
        self.wait_until(dd_csv_xp, type="clickable").click()

    def to_healing_done(self) -> None:
        """Navigate from "damage dealt" to "healing" tab."""
        dd_url = self.driver.current_url
        hd_url = dd_url.replace("&type=damage-done", "&type=healing")

        self.driver.get(hd_url)

        # No need to scroll down again, we stay at the bottom of the page

    def get_healing_done(self) -> None:  # TODO
        """Download csv from healing tab."""
        time.sleep(0.4)

        hd_csv_xp = "//button/span[./text()='CSV']"
        self.wait_until(hd_csv_xp, type="clickable").click()
