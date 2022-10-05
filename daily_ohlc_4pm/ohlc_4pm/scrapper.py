from daily_ohlc_4pm.helpers.logger import return_logger
from bs4 import BeautifulSoup
import re

import uuid

import requests
import sys
sys.path.append("../")

import datetime
from dateutil.tz import gettz
import time

from uuid import uuid4


class getOHLCData():
    '''
        Summary Line
        ------------
            Class to represent Nifty Scrapper

        Methods
        -------
            get_latest_page():
                Return HTML page source of https://www.nseindia.com/
            get_open():
                Returns opening price of Nifty
            get_high():
                Returns high price of Nifty
            get_low():
                Returns low price of Nifty
            get_close():
                Returns closing price of Nifty
            get_change():
                Returns chnage in price of Nifty
            get_change_percentage():
                Returns percentage change in price of Nifty
            get_data():
                Collect all the data from above methods and create entity to write to DB
        '''

    def __init__(self):
        self.logger = return_logger()
        self.url = "https://www.nseindia.com/"
        self.logger.info(f"Starting scrapping for {self.url}")
        self.user_agent = "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"

    def get_latest_page(self):
        status = 500
        soup = ''
        try:
            resp = requests.get(self.url, headers={"User-Agent": self.user_agent})
            if resp.status_code == 200:
                status = 200
                self.logger.info(f"{self.url} returned status code {status}")
            soup = BeautifulSoup(resp.content,'lxml')
        except Exception as e:
            self.logger.warning(f"Failed to get latest NSE website snapshot due to {e}")
        return {'status': status, 'soup': soup}

    def get_open(self, soup):
        value = 0.0
        try:
            value = float(soup.find('span', {'class': 'openVal'}).text.replace(",", "").strip())
        except Exception as e:
            self.logger.warning(f"Failed to get OPEN VALUE due to {e}")
        return value

    def get_high(self, soup):
        value = 0.0
        try:
            value = float(soup.find('span', {'class': 'highVal'}).text.replace(",", "").strip())
        except Exception as e:
            self.logger.warning(f"Failed to get HIGH VALUE due to {e}")
        return value

    def get_low(self, soup):
        value = 0.0
        try:
            value = float(soup.find('span', {'class': 'lowVal'}).text.replace(",", "").strip())
        except Exception as e:
            self.logger.warning(f"Failed to get LOW VALUE due to {e}")
        return value

    def get_close(self, soup):
        value = 0.0
        try:
            value = float(soup.find('span', {'class': 'val'}).text.replace(",", ""))
        except Exception as e:
            self.logger.warning(f"Failed to get CLOSE VALUE due to {e}")
        return value

    def get_change(self, soup):
        value = 0.0
        try:
            value = soup.find('span', {'class': 'val_per'}).text.replace(",", "").strip()
            value = float(re.sub(r"\(.*\)", "", value).strip())
        except Exception as e:
            self.logger.warning(f"Failed to get CHANGE PERCENTAGE due to {e}")
        return value

    def get_change_percentage(self, soup):
        value = 0.0
        try:
            value = soup.find('span', {'class': 'val_per'}).text.replace(",", "")
            matches = re.findall(r"\(.*\)", value)
            if matches:
                value = float(matches[0].strip().replace("(", "").replace(")", "").replace("%", "").strip())
            else:
                value = 0.0
        except Exception as e:
            self.logger.warning(f"Failed to get CHANGE PERCENTAGE VALUE due to {e}")
        return value

    def get_data(self):
        start_time = time.time()
        timestamp = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
        data_entity = {
            'timestamp': timestamp,
            'open': 0.0,
            'high': 0.0,
            'low': 0.0,
            'close': 0.0,
            'nifty_change': 0.0,
            'nifty_change_percentage': 0.0,
            'status': "FAILURE",
            'sr_no' : str(uuid4())
        }
        try:
            params = self.get_latest_page()
            if params.get('status') == 200:
                self.logger.info(f"Latest page scrapping successfull.")
            if params.get('soup'):
                self.logger.info(f"Latest page content collected successfully.")
            data_entity['open'] = self.get_open(params.get('soup'))
            data_entity['high'] = self.get_high(params.get('soup'))
            data_entity['low'] = self.get_low(params.get('soup'))
            data_entity['close'] = self.get_close(params.get('soup'))
            data_entity['nifty_change'] = self.get_change(params.get('soup'))
            data_entity['nifty_change_percentage'] = self.get_change_percentage(params.get('soup'))
            data_entity['status'] = "SUCCESS"
            data_entity['sr_no'] = str(uuid4())
        except Exception as e:
            self.logger.warning(f"Failed to get latest data due to {e}")
        end_time = time.time()
        self.logger.info(f"Time take = {round(end_time - start_time, 2)} seconds")
        return data_entity




