from scraper_api import ScraperAPIClient
client = ScraperAPIClient('352c90489d500e45cab80df55a2033f0')
result = client.get(url = 'https://tinbds.com/du-an/ho-chi-minh/quan-1').text
print(result)
# Scrapy users can simply replace the urls in their start_urls and parse function
# Note for Scrapy, you should not use DOWNLOAD_DELAY and
# RANDOMIZE_DOWNLOAD_DELAY, these will lower your concurrency and are not
# needed with our API