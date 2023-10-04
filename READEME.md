# Github Crawler

A simple crawler to search Github and retrieve the URLs of the search results.

## Installation

1. Clone the repository
2. Create a virtual environment and activate it
3. Install the dependencies using `pip install -r requirements.txt`

## Usage

```python
from github_crawler import GithubCrawler

keywords = ['keyword1', 'keyword2']
search_type = 'Repositories'  # or 'Issues' or 'Wikis'
proxies = ['http://your.proxy.here']  # optional

crawler = GithubCrawler(keywords, search_type, proxies)
urls = crawler.crawl()
print(urls)
