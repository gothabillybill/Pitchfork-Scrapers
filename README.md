# pitchfork-scraper

This is a repository for scrapers for the music review site Pitchfork.com. 

The only scraper here thus far is written with BeautifulSoup, and it creates a database file that stores the average album review score for each artist on the site.
The number of albums scraped depends on the number of pages the user decides to input.

Requirements:
- re
- urllib
- BeautifulSoup
- os.path
- sqlite3
- pickle
