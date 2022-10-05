import sys

from 4pm_daily_ohlc.ohlc_4pm.scrapper import getOHLCData
from 4pm_daily_ohlc.helpers.database import sqlHandling
from 4pm_daily_ohlc.helpers.constants import get_list_of_trading_holidays
from 4pm_daily_ohlc.helpers.logger import return_logger
from datetime import datetime
from dateutil.tz import gettz

if __name__ == '__main__':

    logger = return_logger()
    trading_holidays = get_list_of_trading_holidays()
    trading_holidays = []
    today_date = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%d-%m-%Y")
    if today_date in trading_holidays:
        logger.info('Trading holiday. Skipping scrapping')
    else:
        logger.info('Not a trading holiday.')
        data = getOHLCData().get_data()
        if data.get('status') == "SUCCESS":
            logger.info('Data scrapped succesfully. Pushing to DB')
            sqlHandling().insert(table_name='nifty_ohlc', data=data)
        else:
            data = getOHLCData().get_data()
            if data.get('status') == "SUCCESS":
                logger.info('Data scrapped succesfully. Pushing to DB')
                sqlHandling().insert(table_name='nifty_ohlc', data=data)
            else:
                data = getOHLCData().get_data()
                if data.get('status') == "SUCCESS":
                    logger.info('Data scrapped succesfully. Pushing to DB')
                    sqlHandling().insert(table_name='nifty_ohlc', data=data)
                else:
                    data = getOHLCData().get_data()
                    if data.get('status') == "SUCCESS":
                        logger.info('Data scrapped succesfully. Pushing to DB')
                        sqlHandling().insert(table_name='nifty_ohlc', data=data)
                    else:
                        data = getOHLCData().get_data()
                        if data.get('status') == "SUCCESS":
                            logger.info('Data scrapped succesfully. Pushing to DB')
                            sqlHandling().insert(table_name='nifty_ohlc', data=data)
                        else:
                            data = getOHLCData().get_data()
                            if data.get('status') == "SUCCESS":
                                logger.info('Data scrapped succesfully. Pushing to DB')
                                sqlHandling().insert(table_name='nifty_ohlc', data=data)
                            else:
                                data = getOHLCData().get_data()
                                if data.get('status') == "SUCCESS":
                                    logger.info('Data scrapped succesfully. Pushing to DB')
                                    sqlHandling().insert(table_name='nifty_ohlc', data=data)



