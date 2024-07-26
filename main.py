import requests
import os
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from fp.fp import FreeProxy  # Ensure you have this library installed

import pandas as pd
from io import StringIO

from getter import Getter

from urllib.parse import urlparse, parse_qs

tickers = ['ABIO', 'AFKS', 'AFLT', 'ALRS', 'ASTR', 'CHMF', 'DIAS', 'FEES', 'GMKN', 'IRAO', 'MAGN', 'MGNT', 'MOEX', 'MSNG', 'MTLR', 'MTSS', 'NLMK', 'NVTK', 'PHOR', 'PIKK', 'PLZL', 'POSI', 'ROSN', 'RTKM', 'RUAL', 'SBERP', 'SMLT', 'SNGS', 'SNGSP', 'SVCB', 'TATN', 'TATNP', 'VKCO', 'VTBR']

class OptionDataDownloader:
    def __init__(self, service=None):
        self.dir = None
        self.service=service # Do not create multiple services
    
    def download(self, ticker, dir):
        url = f'https://www.moex.com/ru/derivatives/optionsdesk.aspx?code={ticker}&sid=1&sby=1&c4=on&submit=submit'
        csv_links = self._get_csv_links(url)
        
        for link in csv_links:
            OptionDataDownloader._download_option_data(csv_link=link, base_url=url, dir=dir)
            
    def _get_csv_links(self, url):
        """Takes the url of MOEX webpage and extracts links to csv with options' data from the url"""
        html_content = Getter(use_proxy=True, use_selenium=True, service=self.service).get(url = url) # Do not create multiple services
        soup = BeautifulSoup(html_content, 'html.parser')

        links = soup.find_all('a', href=True)

        csv_links = [link for link in links if 'CSV' in (link.get_text() or '')]
        
        return csv_links

    @staticmethod
    def _response2df(response):
        """Makes pandas DataFrame from response object"""
        data = StringIO(response.text)
        df = pd.read_csv(data, header=0)
        return df

    @staticmethod
    def _save_response(response, dir, file):
        """Saves response object at dir/file path"""
        df = OptionDataDownloader._response2df(response)
        
        output_dir = Path(dir)
        output_file = file
        
        output_dir.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_dir / output_file)
        
    @staticmethod
    def _download_option_data(csv_link, base_url, dir):
        csv_url = csv_link['href']
        
        print(f'Processing {csv_url}')
        
        # Handle relative URLs
        if not csv_url.startswith('http'):
            csv_url = f'https://{base_url.split("/")[2]}{csv_url}'
        
        
        # Extract Option parameters from the URL
        parsed_url = urlparse(csv_url)
        query_params = parse_qs(parsed_url.query)
        ticker = query_params.get('code', [None])[0]
        expiration_date = query_params.get('delivery', [None])[0]
        
        if query_params.get('type', [None])[0] != '2': #The second type of csv link; ignore
            try:            
                response = Getter(use_proxy=False, use_selenium=False, verify=True).get(csv_url)
                if not response.content:
                    print(f'Failed to load content for {expiration_date}')
                    raise BaseException(f'CustomError: {csv_url}')
                OptionDataDownloader._save_response(
                    response=response,
                    dir=dir,
                    file=f'{expiration_date}.csv'
                    )
                
                print(f'Downloaded successfully CSV file for {expiration_date} .')
                
                
            except requests.RequestException as e:
                print(f"Requests exception occurred for {expiration_date}: {e}")
                raise e
            
def fetch_moex_data(tickers, path='data'):
    """Parse options trading data from MOEX website into path/ticker/expiration_date.csv"""
    service = Service(GeckoDriverManager().install())
    odd = OptionDataDownloader(service=service)

    for ticker in tickers:
        print('<_______________________')
        try:
            odd.download(ticker=ticker, dir=f'{path}/{ticker}')
            print(f'Downloaded data for {ticker} successfully')
        except:
            print(f'Error occured when processing {ticker}')
        print('_______________________>')
        
        
if __name__ == '__main__':
    fetch_moex_data(tickers=tickers)