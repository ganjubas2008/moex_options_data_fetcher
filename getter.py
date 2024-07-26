import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from fp.fp import FreeProxy


class Getter:
    def __init__(self, use_proxy=True, use_selenium=True, headers=None, verify=False, service=None):
        self.use_proxy = use_proxy
        self.use_selenium = use_selenium
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.verify = verify
        self.service = service  # Do not create multiple services

    def get(self, url):
        """Retrieve HTML content from a URL, using proxy and/or Selenium as specified."""
        if self.use_selenium:
            return self._get_with_selenium(url)
        else:
            return self._get_with_requests(url)

    def _get_with_requests(self, url):
        """Retrieve HTML content using requests, optionally with a proxy."""
        proxies = None
        if self.use_proxy:
            try:
                proxy = FreeProxy(rand=True, country_id=['RU'], elite=True).get()
                proxies = {"http": proxy, "https": proxy}
                print(f"Using proxy: {proxy}")
            except Exception as e:
                print(f"Failed to obtain a proxy: {e}")

        try:
            response = requests.get(url, proxies=proxies, headers=self.headers, verify=self.verify)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Requests exception occurred: {e}")
            return None

    def _get_with_selenium(self, url):
        """Retrieve HTML content using Selenium, optionally with a proxy."""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        if self.use_proxy:
            try:
                proxy = FreeProxy(rand=True, country_id=['RU'], elite=True).get()
                options.add_argument(f'--proxy-server={proxy}')
                print(f"Using proxy: {proxy}")
            except Exception as e:
                print(f"Failed to obtain a proxy: {e}")

        try:
            service = self.service or Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            driver.get(url)
            html = driver.page_source
            driver.quit()
            return html
        except WebDriverException as e:
            print(f"WebDriverException occurred: {e}")
            return None
        finally:
            try:
                driver.quit()
            except Exception as e:
                print(f"Failed to quit driver: {e}")
