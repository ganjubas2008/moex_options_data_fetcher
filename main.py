import time
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from src.option_data_downloader import OptionDataDownloader

def fetch_moex_data(tickers, path='data'):
    """Download options trading data from MOEX website and save to CSV files."""
    service = Service(GeckoDriverManager().install())
    odd = OptionDataDownloader(service=service)

    for ticker in tickers:
        print('<_______________________')
        try:
            odd.download(ticker=ticker, dir=f'{path}/{ticker}')
            print(f'Downloaded data for {ticker} successfully')
        except Exception as e:
            print(f'Error occurred when processing {ticker}: {e}')
        print('_______________________>')


if __name__ == '__main__':
    tickers = [
        'ABIO', 'AFKS', 'AFLT', 'ALRS', 'ASTR', 'CHMF', 'DIAS', 'FEES', 'GMKN', 'IRAO', 'MAGN', 'MGNT',
        'MOEX', 'MSNG', 'MTLR', 'MTSS', 'NLMK', 'NVTK', 'PHOR', 'PIKK', 'PLZL', 'POSI', 'ROSN', 'RTKM',
        'RUAL', 'SBERP', 'SMLT', 'SNGS', 'SNGSP', 'SVCB', 'TATN', 'TATNP', 'VKCO', 'VTBR'
    ]
    
    while True:
        fetch_moex_data(tickers=tickers)
        time.sleep(900)  # Sleep for 15 minutes (900 seconds)
