"""
An abstraction for creating and handling a bunch of random people.
"""

import string
from typing import Self
from random import choices, randint

NB_PERSON = 10
AGES = (20, 22)
NAME_SIZES = (2, 5)
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
    """Generator to generate unique string"""

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
