from sqlalchemy import inspect, create_engine
import os
import sys
sys.path.append('../')
from nifty_ohlc_scrappers.helpers.logger import return_logger
from nifty_ohlc_scrappers.helpers.tables import nifty_ohlc,nseindia_nifty
from sqlalchemy.orm import sessionmaker


class sqlHandling():
    '''
    Summary Line
    -----------
        Class to represent handling sql database

    Attributes
    ---------
        None

    Methods
    ------
        insert(table_name,data):
            Inserts data into table_name. Creates table if does not exist.
    '''

    def __init__(self):
        '''
        Summary Line
        ------------
            Constructs connections to DB, enables connection pooling, inspects tables, creates session
        '''
        self.logger = return_logger() # logging
        self.user = 'nse_test' # db user
        self.password = 'nse@123' # db password
        self.database = 'FRONTDB' # db name
        self.host = '0.0.0.0' # db host
        self.engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}'
                                    ,pool_size=20, max_overflow=0) #Connection pooling to avoid locking
        self.inspector = inspect(self.engine) # Inspector to inspect tables before creating
        Session = sessionmaker(bind=self.engine) # Binds connectin pool with Session
        self.session = Session() # Creates session with DB


    def insert(self,table_name,data):

        '''
        Summary Line
        ------------
            Inserts data into table. Creates table if not exist with schema from tables.py
        :param
            table_name: Name of the table to insert into
        :param
            data: Values to insert
        :return:
            None
        '''

        try:
            if table_name == 'nifty_ohlc':
                if table_name not in self.engine.table_names():
                    nifty_ohlc.__table__.create(bind = self.engine,checkfirst = True)
                row = nifty_ohlc(data.get('timestamp'),
                                 data.get('open'),data.get('high'),
                                 data.get('low'),data.get('close'),
                                 data.get('nifty_change'),data.get('nifty_change_percentage'))
                self.session.add(row)
                self.session.commit()
                self.logger.info(f"Data inserted successsfully for table {table_name}.")
            elif table_name == 'nseindia_nifty':
                if table_name not in self.engine.table_names():
                    nseindia_nifty.__table__.create(bind = self.engine,checkfirst = True)

                row = nseindia_nifty(data.get('timestamp'),data.get('timestamp_create'),
                                     data.get('open'), data.get('high'),
                                     data.get('low'), data.get('close'),
                                     data.get('nifty_change'), data.get('nifty_change_percentage')
                                     )
                self.session.add(row)
                self.session.commit()
                self.logger.info(f"Data inserted successsfully for table {table_name}.")
        except Exception as e:
            self.logger.error('Duplicate entries not allowed. Skipping')
        self.session.close()
        self.logger.info('Session closed.')
