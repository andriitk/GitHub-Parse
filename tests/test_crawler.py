import unittest
import requests
from unittest.mock import patch, Mock
from github_crawler.crawler import GithubCrawler


class TestGithubCrawler(unittest.TestCase):

    @patch('github_crawler.crawler.requests.get')
    def test_crawl_without_proxies(self, mock_get):
        # Mock the response for a basic search
        mock_response = Mock()
        mock_response.content = b'<a class="v-align-middle" href="/test/repo1"></a>'
        mock_get.return_value = mock_response

        crawler = GithubCrawler(['test'], 'Repositories')
        results = crawler.crawl()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['url'], 'https://github.com/test/repo1')

    @patch('github_crawler.crawler.requests.get')
    def test_crawl_with_proxies(self, mock_get):
        # Mock the response for a basic search
        mock_response = Mock()
        mock_response.content = b'<a class="v-align-middle" href="/test/repo2"></a>'
        mock_get.return_value = mock_response

        crawler = GithubCrawler(['test'], 'Repositories', proxies=['http://example.com:8080'])
        results = crawler.crawl()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['url'], 'https://github.com/test/repo2')

    @patch('github_crawler.crawler.requests.get')
    def test_get_repo_details(self, mock_get):
        # Mock the response for repo details
        mock_response = Mock()
        mock_response.content = b'''
        <span class="author"><a href="/author_name">Author</a></span>
        <ol class="repository-lang-stats-numbers">
            <li><span class="lang">Python</span> <span class="percent">70%</span></li>
            <li><span class="lang">JavaScript</span> <span class="percent">30%</span></li>
        </ol>
        '''
        mock_get.return_value = mock_response

        crawler = GithubCrawler(['test'], 'Repositories')
        details = crawler._get_repo_details('https://github.com/test/repo')
        self.assertEqual(details['owner'], 'Author')
        self.assertDictEqual(details['languages'], {'Python': '70%', 'JavaScript': '30%'})

    @patch('github_crawler.crawler.requests.get')
    def test_request_with_retry_failure(self, mock_get):
        # Mock a failed response
        mock_get.side_effect = requests.RequestException
        crawler = GithubCrawler(['test'], 'Repositories')

        with self.assertRaises(Exception):
            crawler._request_with_retry('https://github.com/test/repo')


if __name__ == '__main__':
    unittest.main()
