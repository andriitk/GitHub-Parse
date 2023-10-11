# Github Crawler

A simple crawler to search Github and retrieve the URLs of the search results.

## Installation

1. Clone the repository: `git clone https://github.com/andriitk/GitHub-Parse.git`
2. Navigate to the project directory: `cd path_to_project`
3. Install the dependencies using `pip install -r requirements.txt`

## Usage

```python
from github_crawler.crawler import GithubCrawler

keywords = ["keyword1", "keyword2"]
search_type = "Repositories"  # can be "Repositories", "Wikis", or "Issues"
proxies = ["http://example.com:8080", "http://example2.com:8080"]  # optional

crawler = GithubCrawler(keywords, search_type, proxies)
urls = crawler.crawl()
print(urls)
```

## Running the Tests
To run the tests, execute the following command in the project's root directory:

`python -m unittest discover`
