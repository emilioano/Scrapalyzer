import pytest

from modules.scraper.scraper import Scraper

#Testing fetch image function from Scraper class
def test_fetch_image():
    test_url = 'https://www.pexels.com/search/animal/'
    scraper = Scraper(test_url)
    urls = scraper.fetch_image()
    #It should return a list
    assert isinstance(urls, list)
    #Confirm that the function returns something valid (list)
    assert len(urls) >= 0
    #All items should be returned as strings
    assert all(isinstance(u, str)for u in urls)
    