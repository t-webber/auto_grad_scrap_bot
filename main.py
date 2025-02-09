"""
Runner for the project
"""

from people import People
from scraper import AgeScraper, PeopleScraper

def main():
    """Main function to be run"""
    people = People.random()
    scraper = PeopleScraper(people.people)
    if not scraper.insert_age():
        print("Insertion failed. No button was found.")
    print(AgeScraper(20).list_people())

if __name__ == "__main__":
    main()
