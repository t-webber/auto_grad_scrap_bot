"""
An abstraction for creating and handling a bunch of random people.
"""

import string
from random import choices, randint
from typing import Self

from config import AGE_RANGE, GENERATION_TRY_LIMIT, NAME_LENGTHS, NB_PERSON


class UniqueStringGenerator:
    """Generator to generate unique string"""

    LENGTHS: tuple[int, int] = NAME_LENGTHS
    TRY_LIMIT: int = GENERATION_TRY_LIMIT

    def __init__(self):
        self.history: list[str] = []

    @classmethod
    def __random_string(cls):
        """Generates a random string"""
        return ''.join(choices(string.ascii_letters, k=randint(*cls.LENGTHS)))

    def generate(self) -> str:
        """Generates a random string that has never been generated before"""
        random = self.__random_string()
        for _ in range(self.TRY_LIMIT):
            if random not in self.history:
                return random
            random = self.__random_string()
        raise ValueError("Failed to create another string with those params.")


class Person:
    """Represents one person"""

    ages: tuple[int, int] = AGE_RANGE

    def __init__(self, first_name: str, last_name: str, age: int):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __repr__(self) -> str:
        """Representation used for logging"""
        return f"\n\t{self.first_name} {self.last_name}, {self.age} years old"

    @classmethod
    def random(cls, gen: UniqueStringGenerator) -> Self:
        """Generates a random person"""
        return Person(gen.generate(), gen.generate(), randint(*cls.ages))


class People:
    """Represents a population of people"""

    length: int = NB_PERSON

    def __init__(self, people: list[Person]):
        self.people = people

    @classmethod
    def random(cls) -> Self:
        """Generates a random person"""
        gen = UniqueStringGenerator()
        return People([Person.random(gen) for _ in range(cls.length)])

    def filter_by_age(self) -> dict[int, list[Person]]:
        """Returns the people of a given age"""
        generations = {}
        for person in self.people:
            if generations.get(person.age) is None:
                generations[person.age] = [person]
            else:
                generations[person.age].append(person)
        return generations

    def __repr__(self) -> str:
        """Representation used for logging"""
        return f"[{"".join(map(repr, self.people))}\n]"
