"""
Runner for the project
"""

from people import People
from scraper import PeopleScraper


def main():
    """Main function to be run"""
    people = People.random()
    print("People = ", people)
    scraper = PeopleScraper(people)
    if not scraper.insert_age():
        print("Insertion failed. No button was found.")
    if not scraper.check_ages():
        print("Ages check failed. Invalid /age page.")


if __name__ == "__main__":
    main()
