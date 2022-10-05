import sys
sys.path.append("../")
import time
from nifty_ohlc_scrappers.nifty_option_chains.scrapper import getOptionsData
from nifty_ohlc_scrappers.helpers.database import sqlHandling
from nifty_ohlc_scrappers.helpers.constants import get_list_of_trading_holidays
from nifty_ohlc_scrappers.helpers.logger import return_logger
from datetime import datetime
from dateutil.tz import gettz
import pandas as pd


def get_final_data():
    puts, calls, status = getOptionsData().get_curated_data()
    return puts,calls,status

if __name__ == '__main__':
    logger = return_logger()
    trading_holidays = get_list_of_trading_holidays() # Get list of trading holidays
    optionsObj = getOptionsData()
    expiry_dates, status = optionsObj.get_expiry_dates()
    if status == 'SUCCESS':
        expiry_df = pd.DataFrame({'expiry_date':expiry_dates})
        sqlHandling().insert_dataframe(table_name='expiry_dates', dataframe=expiry_df)
        logger.info("Inserted expiry dates.")



    while True:
        today_date = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%d-%m-%Y")
        if today_date in trading_holidays:
            logger.info('Trading holiday. Skipping scrapping')
        else:
            logger.info('Not a trading holiday.')
            puts,calls,status = get_final_data()
            if status == "SUCCESS":
                sqlHandling().insert_dataframe(table_name='nseindia_optionchain', dataframe = puts)
                sqlHandling().insert_dataframe(table_name='nseindia_optionchain', dataframe = calls)
                sleeping_time = 30
            else:
                sleeping_time = 1
        logger.info(f"Sleeping for {sleeping_time} seconds..")
        time.sleep(sleeping_time)  #Scrape again after 30 seconds