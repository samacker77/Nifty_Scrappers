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
        '''

        :param date: date of scrapping
        :param open: opening price
        :param high: highest price
        :param low: lowest price
        :param close: closing price
        :param nifty_change: change in price
        :param nifty_change_percentage: percentage change
        '''
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


class nseindia_optionchain(Base):
    '''
        nifty_ohlc tables as class with schema defined
    '''

    __tablename__ = 'nseindia_optionchain'
    id = Column(Integer,Sequence('id'),primary_key=True,nullable=False)
    timestamp = Column(DateTime)
    timestamp_create = Column(DateTime)
    contract = Column(String(100))
    ltp = Column(Float)
    ltp_net_chng = Column(Float)
    volume = Column(Integer)
    oi = Column(Float)
    underlying = Column(String(20))
    expiry = Column(Date)
    contract_type = Column(String(10))
    strike_price = Column(Float)
    days_to_expiry = Column(Float)
    delta = Column(Float)
    gamma = Column(Float)
    theta = Column(Float)
    vega = Column(Float)
    rho = Column(Float)

    def __init__(self,timestamp,timestamp_create,contract,ltp,ltp_net_change,volume,oi,underlying,expiry,
                 contract_type,strike_price,days_to_expiry,delta,gamma,theta,vega,rho):

        '''

        :param timestamp: time of scraping
        :param timestamp_create: time of ingestion
        :param contract: contract
        :param ltp: last traded price
        :param ltp_net_change: change in last traded price
        :param volume: volume
        :param oi: open interest
        :param underlying: underlying stock
        :param expiry: expiry
        :param contract_type: contract type
        :param strike_price: strike price
        :param days_to_expiry: number of days until expiry
        :param delta: delta
        :param gamma: gamma
        :param theta: theta
        :param vega: vega
        :param rho: rho
        '''
        self.timestamp = timestamp
        self.timestamp_create = timestamp_create
        self.contract = contract
        self.ltp = ltp
        self.ltp_net_change = ltp_net_change
        self.volume = volume
        self.oi = oi
        self.underlying = underlying
        self.expiry = expiry
        self.contract_type = contract_type
        self.strike_price = strike_price
        self.days_to_expiry = days_to_expiry
        self.delta = delta
        self.gamma = gamma
        self.theta = theta
        self.vega = vega
        self.rho = rho



class expiry_dates(Base):
    '''
        nifty_ohlc tables as class with schema defined
    '''

    __tablename__ = 'expiry_dates'
    expiry_date = Column(Date,primary_key=True)


    def __init__(self,expiry_date):
        '''

        :param expiry_date:
        '''

        self.expiry_date = expiry_date