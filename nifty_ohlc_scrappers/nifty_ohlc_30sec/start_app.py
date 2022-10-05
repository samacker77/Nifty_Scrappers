import sys
sys.path.append("../")
import time
from nifty_ohlc_scrappers.nifty_ohlc_30sec.scrapper import getOHLCData
from nifty_ohlc_scrappers.helpers.database import sqlHandling
from nifty_ohlc_scrappers.helpers.constants import get_list_of_trading_holidays
from nifty_ohlc_scrappers.helpers.logger import return_logger
from datetime import datetime
from dateutil.tz import gettz

if __name__ == '__main__':
    logger = return_logger()
    trading_holidays = get_list_of_trading_holidays() # Get list of trading holidays
    today_date = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%d-%m-%Y")
    if today_date in trading_holidays:
        logger.info('Trading holiday. Skipping scrapping')
    else:
        while True:
            logger.info('Not a trading holiday.')
            data = getOHLCData().get_data()
            if data.get('status') == "SUCCESS":
                sqlHandling().insert(table_name='nseindia_nifty', data=data)
                sleeping_time = 30
            else:
                sleeping_time = 1
            logger.info("Sleeping for 30 seconds..")
            time.sleep(sleeping_time)