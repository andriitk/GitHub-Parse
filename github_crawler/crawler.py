import requests
from bs4 import BeautifulSoup
import random

GITHUB_BASE_URL = 'https://github.com/search?q={query}&type={type}'


class GithubCrawler:
    def __init__(self, keywords, search_type, proxies=None):
        self.keywords = keywords
        self.search_type = search_type
        self.proxies = proxies or []

    def _get_random_proxy(self):
        return random.choice(self.proxies) if self.proxies else None

    def _get_repo_details(self, repo_url):
        response = requests.get(repo_url, proxies={'http': self._get_random_proxy(), 'https': self._get_random_proxy()})
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract owner details
        owner = soup.select_one('span.author a').text.strip()

        # Extract language stats
        lang_stat_elements = soup.select('span.d-inline > span[itemprop="programmingLanguage"]')
        lang_stats = [lang.text.strip() for lang in lang_stat_elements]

        return {
            'owner': owner,
            'languages': lang_stats
        }

    def crawl(self):
        query = '+'.join(self.keywords)
        url = GITHUB_BASE_URL.format(query=query, type=self.search_type)
        response = requests.get(url, proxies={'http': self._get_random_proxy(), 'https': self._get_random_proxy()})
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        urls = [link['href'] for link in soup.select('a.v-align-middle')]

        results = []
        for url in urls:
            full_url = 'https://github.com' + url
            if self.search_type == 'Repositories':
                repo_details = self._get_repo_details(full_url)
                results.append({
                    'url': full_url,
                    'owner': repo_details['owner'],
                    'languages': repo_details['languages']
                })
            else:
                results.append({
                    'url': full_url
                })

        return results
