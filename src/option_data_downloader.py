from bs4 import BeautifulSoup
# from selenium.webdriver.firefox.service import Service
from urllib.parse import urlparse, parse_qs
import pandas as pd
from io import StringIO
from pathlib import Path
from src.getter import Getter


class OptionDataDownloader:
    def __init__(self, service=None):
        self.service = service  # Do not create multiple services

    def download(self, ticker, dir):
        url = f'https://www.moex.com/ru/derivatives/optionsdesk.aspx?code={ticker}&sid=1&sby=1&c4=on&submit=submit'
        csv_links = self._get_csv_links(url)

        for link in csv_links:
            self._download_option_data(csv_link=link, base_url=url, dir=dir)

    def _get_csv_links(self, url):
        """Extract links to CSV files with options data from the URL."""
        html = Getter(use_proxy=True, use_selenium=False, service=self.service, verify=True).get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        links = soup.find_all('a', href=True)
        csv_links = [link for link in links if 'CSV' in (link.get_text() or '')]
        return csv_links

    @staticmethod
    def _response2df(response):
        """Convert response content to a pandas DataFrame."""
        data = StringIO(response.text)
        df = pd.read_csv(data, header=0)
        return df

    @staticmethod
    def _save_response(response, dir, file):
        """Save the response content to a CSV file."""
        df = OptionDataDownloader._response2df(response)
        output_dir = Path(dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_dir / file, index=False)

    def _download_option_data(self, csv_link, base_url, dir):
        csv_url = csv_link['href']
        if not csv_url.startswith('http'):
            csv_url = f'https://{base_url.split("/")[2]}{csv_url}'

        parsed_url = urlparse(csv_url)
        query_params = parse_qs(parsed_url.query)
        ticker = query_params.get('code', [None])[0]
        expiration_date = query_params.get('delivery', [None])[0]

        if query_params.get('type', [None])[0] != '2':
            try:
                response = Getter(use_proxy=False, use_selenium=False, verify=True).get(csv_url)
                if not response or not response.content:
                    print(f'Failed to load content for {expiration_date}')
                    return
                self._save_response(response, dir, f'{expiration_date}.csv')
                print(f'Downloaded successfully CSV file for {expiration_date}.')
            except requests.RequestException as e:
                print(f"Requests exception occurred for {expiration_date}: {e}")
