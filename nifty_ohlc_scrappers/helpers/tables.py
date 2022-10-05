from sqlalchemy import create_engine, Column, Integer, Sequence, String, Date, Float, BIGINT,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class nifty_ohlc(Base):
    '''
        nifty_ohlc tables as class with schema defined
    '''

    __tablename__ = 'nifty_ohlc'
    sr_no = Column(Integer,Sequence('sr_no'),primary_key=True)
    date = Column(Date,unique=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    nifty_change = Column(Float)
    nifty_change_percentage = Column(Float)

    def __init__(self,date,open,high,low,close,nifty_change,nifty_change_percentage):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.nifty_change = nifty_change
        self.nifty_change_percentage = nifty_change_percentage


class nseindia_nifty(Base):

    __tablename__ = 'nseindia_nifty'
    id = Column(Integer,Sequence('id'),primary_key=True,nullable=False)
    timestamp = Column(DateTime)
    timestamp_create = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    nifty_change = Column(Float)
    nifty_change_percentage = Column(Float)

    def __init__(self,timestamp,timestamp_create,open,high,low,close,nifty_change,nifty_change_percentage):
        '''
        Summary Line
        ------------
            Mapping data to attributes

        :param timestamp:
            time of scrapping
        :param timestamp_create:
            time of ingestion
        :param open:
            nifty open
        :param high:
            nifty high
        :param low:
            nifty low
        :param close:
            nifty close
        :param nifty_change:
            nifty change amount
        :param nifty_change_percentage:
            nifty change percentage
        '''
        self.timestamp = timestamp
        self.timestamp_create = timestamp_create
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.nifty_change = nifty_change
        self.nifty_change_percentage = nifty_change_percentage
