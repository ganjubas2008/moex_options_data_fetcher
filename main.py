import time
from datetime import datetime, timedelta
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from src.option_data_downloader import OptionDataDownloader

def fetch_moex_data(tickers, base_path='data'):
    """Download options trading data from MOEX website and save to CSV files."""
    service = Service(GeckoDriverManager().install())
    odd = OptionDataDownloader(service=service)
    
    now = datetime.now()
    rounded_minute = (now.minute // 15) * 15
    rounded_time = now.replace(minute=rounded_minute, second=0, microsecond=0)
    timestamp = rounded_time.strftime('%Y%m%d_%H%M')

    for ticker in tickers:
        print('<_______________________')
        try:
            path = f'{base_path}/{timestamp}/{ticker}'
            odd.download(ticker=ticker, dir=path)
            print(f'Downloaded data for {ticker} successfully')
        except Exception as e:
            print(f'Error occurred when processing {ticker}: {e}')
        print('_______________________>')

def wait_until_next_interval():
    """Wait until the next 00, 15, 30, or 45 minute interval."""
    now = datetime.now()
    next_minute = (now.minute // 15 + 1) * 15
    if next_minute == 60:
        next_minute = 0
        next_hour = now.hour + 1
        next_time = now.replace(hour=next_hour, minute=next_minute, second=0, microsecond=0)
    else:
        next_time = now.replace(minute=next_minute, second=0, microsecond=0)
    
    wait_time = (next_time - now).total_seconds()
    print(f"Waiting for {wait_time} seconds until the next interval.")
    time.sleep(max(0, wait_time))

if __name__ == '__main__':
    tickers = [
        'ABIO', 'AFKS', 'AFLT', 'ALRS', 'ASTR', 'CHMF', 'DIAS', 'FEES', 'GMKN', 'IRAO', 'MAGN', 'MGNT',
        'MOEX', 'MSNG', 'MTLR', 'MTSS', 'NLMK', 'NVTK', 'PHOR', 'PIKK', 'PLZL', 'POSI', 'ROSN', 'RTKM',
        'RUAL', 'SBERP', 'SMLT', 'SNGS', 'SNGSP', 'SVCB', 'TATN', 'TATNP', 'VKCO', 'VTBR'
    ]
    
    while True:
        fetch_moex_data(tickers=tickers)
        wait_until_next_interval()
