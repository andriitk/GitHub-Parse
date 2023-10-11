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
        return {
            'http': random.choice(self.proxies),
            'https': random.choice(self.proxies)
        } if self.proxies else {}

    def _request_with_retry(self, url, max_retries=3):
        for _ in range(max_retries):
            try:
                proxies = self._get_random_proxy()
                response = requests.get(url, proxies=proxies, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException:
                continue
        raise Exception("Failed to fetch URL after multiple retries")

    def _get_repo_details(self, repo_url):
        response = self._request_with_retry(repo_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract owner details
        owner_element = soup.select_one('span.author a')
        owner = owner_element.text.strip() if owner_element else "N/A"

        # Extract language stats
        lang_stat_elements = soup.select('ol.repository-lang-stats-numbers li')
        lang_stats = {}
        for lang in lang_stat_elements:
            language_name = lang.select_one('span.lang').text.strip()
            percentage = lang.select_one('span.percent').text.strip()
            lang_stats[language_name] = percentage

        return {
            'owner': owner,
            'languages': lang_stats
        }

    def crawl(self):
        query = '+'.join(self.keywords)
        url = GITHUB_BASE_URL.format(query=query, type=self.search_type)
        response = self._request_with_retry(url)

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
