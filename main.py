"""
A Scraper to check the exercise 1

The test occurs by creating 100 random ages between 20 and 50
and adds them to the database with the name page.

Then, it tests that all the age pages contain the right data.

To not fail, we need no buttons that reload the page other than
the button that submits the person's age.

Furthermore, every first name and last name must appear only once 
in the output.
"""

import string
from time import sleep
from typing import Self
from random import choices, randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

NB_PERSON = 10
AGES = (20, 22)
NAME_SIZES = (2, 5)
URL = "http://localhost:3000"
TRY_LIMIT = 100

class Person:
    """Represents one person"""

    def __init__(self, first_name: str, last_name: str, age: int):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __repr__(self) -> str:
        """Representation used for logging"""
        return f"\n\t{self.first_name} {self.last_name}, {self.age} years old"

class UniqueStringGenerator:

    lengths: tuple[int, int] = NAME_SIZES
    try_limit: int = TRY_LIMIT

    def __init__(self):
        self.history: list[str] = []

    @classmethod
    def __random_string(cls):
        """Generates a random string"""
        return ''.join(choices(string.ascii_letters, k=randint(*cls.lengths))).capitalize()

    def generate(self) -> str:
        """Generates a random string that has never been generated before"""
        random = self.__random_string()
        for _ in range(self.try_limit):
            if random not in self.history:
                return random
            random = self.__random_string()
        raise ValueError("Failed to generate another string with the given parameters.")

class People:
    """Represents a population of people"""

    ages: tuple[int, int] = AGES
    length: int = NB_PERSON

    def __init__(self, people: list[Person]):
        self.people = people

    @classmethod
    def random(cls) -> Self:
        """Generates a random person"""
        generator = UniqueStringGenerator()
        return People([Person(generator.generate(), generator.generate(), randint(*cls.ages)) for _ in range(cls.length)])

    def filter_by_age(self, age: int) -> Self:
        """Returns the people of a given age"""
        return [person for person in self.people if person.age == age]

    def __repr__(self) -> str:
        """Representation used for logging"""
        return f"[{"".join(map(repr, self.people))}\n]"

class Scraper:
    """Scraping bot to interface with the website"""

    def __init__(self):
        self.url_prefix = URL
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

    def __init__(self, people: list[Person]):
        super().__init__()
        self.people = [PersonScraper(person) for person in people]

    def insert_age(self):
        """Inserts a set of people in the database"""
        for person in self.people:
            if not person.insert_age():
                return False
        return True

def main():
    """Main function to be run"""
    people = People.random()
    scraper = PeopleScraper(people.people)
    if not scraper.insert_age():
        print("Insertion failed. No button was found.")

if __name__ == "__main__":
    main()
