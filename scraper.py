"""
An abstraction for directing the scraping bot.
"""

import re
from time import sleep

from config import WEBSITE_URL
from people import People, Person
from selenium import webdriver
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException)
from selenium.webdriver.common.by import By


class Scraper:
    """Scraping bot to interface with the website"""

    def __init__(self):
        self.url_prefix = WEBSITE_URL
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(0.5)

    def find_input(self) -> int:
        """Finds an input in the page"""
        return self.driver.find_element(by=By.TAG_NAME, value="input")

    def page(self, url_path: str):
        """Loads a given page"""
        self.driver.get(f"{self.url_prefix}/{url_path}")


class PersonScraper(Scraper):
    """Scraping bot api for usage on one person"""

    def __init__(self, person: Person):
        super().__init__()
        self.person = person

    def page_name(self):
        """Loads the page /name"""
        self.page(f"name/{self.person.first_name}/{self.person.last_name}")

    def insert_age(self) -> bool:
        """Inserts a person in the database"""
        print(f"Inserting {self.person}")
        self.page_name()
        # <input />
        self.find_input().send_keys(self.person.age)
        sleep(0.5)
        # <button />
        buttons = self.driver.find_elements(by=By.TAG_NAME, value="button")
        for button in buttons:
            try:
                button.click()
            except ElementNotInteractableException:
                pass
        return self.has_age()

    def has_age(self) -> bool:
        """Checks if a person has an age"""
        self.page_name()
        try:
            self.find_input().send_keys("test")
            return False
        except NoSuchElementException:
            return True


class PeopleScraper(Scraper):
    """Scraping bot api for usage on multiple people"""

    def __init__(self, people: People):
        super().__init__()
        self.people = people

    def insert_age(self):
        """Inserts a set of people in the database"""
        for person in self.people.people:
            if not PersonScraper(person).insert_age():
                return False
        return True

    def check_ages(self) -> bool:
        """Checks that the /age pages contain the correct data"""
        generations = self.people.filter_by_age()
        for (age, generation) in generations.items():
            if not PeopleScraper.check_age(age, generation):
                return False
        return True

    @staticmethod
    def check_age(age: int, generation: list[Person]) -> bool:
        """Checks that the /age page is correct for the given age"""
        age_page = AgeScraper(age).list_people()
        for person in generation:
            if find_unique_word(person.first_name, age_page):
                continue
            print(f"\n> Problem for age {age}: {person} has problems.")
            return False
        return True


class AgeScraper(Scraper):
    """Scraping bot for the /age pages"""

    def __init__(self, age: int):
        super().__init__()
        self.age = age

    def page_age(self):
        """Loads the page age/"""
        self.page(f"age/{self.age}")

    def list_people(self) -> str:
        """List all people of the given age"""
        self.page_age()
        return self.driver.find_element(By.TAG_NAME, "body").text


def find_unique_word(word: str, page: str):
    """Checks if there is a unique occurrence"""
    return len(re.findall(r'\b' + re.escape(word) + r'\b', page)) == 1
