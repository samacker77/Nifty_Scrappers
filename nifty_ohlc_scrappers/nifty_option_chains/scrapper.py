import sys
sys.path.append("../")
from nifty_ohlc_scrappers.helpers.logger import return_logger
from datetime import datetime
from dateutil.tz import gettz
import numpy as np
from scipy.stats import norm
import pandas as pd
import requests
import math
from math import pi
import json

class getOptionsData():

    def __init__(self):
        self.logger = return_logger()
        self.url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
        self.logger.info(f"Starting scrapping for {self.url}")
        self.headers = {"user-agent" : "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36",
                        "accept-encoding" : "gzip,deflate,br"}

    def N(self,z):
        '''
        Normal cumulative density function which returns the
        cumulative density under the normal curve along the
        point 'z' where the cumulative density is calculated.
        Refer to scipy.stats documentation for more information
        '''

        return norm.cdf(z)

    def call_delta(self,S, K, r, t, vol):
        '''
        Black-Scholes Call Delta.
        Partial derivative of the option value
        with respect to the change in the underlying stock price.
        Delta measures how the underlying option moves
        with respect to moves in the underlying stock.
        :param S: underlying stock price
        :param K: strike price
        :param r: risk free rate
        :param t: time to expiration
        :param vol: volatility
        '''
        d1 = (1 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
        return self.N(d1)

    def phi(self,x):
        '''
        Phi Helper Function.
        '''
        return np.exp(-0.5 * x ** 2) / (math.sqrt(2.0 * pi))

    def call_delta(self,S, K, r, t, vol):
        '''
        Black-Scholes Call Delta.
        Partial derivative of the option value
        with respect to the change in the underlying stock price.
        Delta measures how the underlying option moves
        with respect to moves in the underlying stock.

        :param S: underlying stock price
        :param K: strike price
        :param r: risk free rate
        :param t: time to expiration
        :param vol: volatility
        '''
        d1 = (1 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
        return self.N(d1)

    def put_delta(self,S, K, r, t, vol):
        '''
        Black-Scholes Put Delta.
        Partial derivative of the option value
        with respect to the change in the underlying stock price.
        Delta measures how the underlying option moves
        with respect to moves in the underlying stock.

        :param S: underlying stock price
        :param K: strike price
        :param r: risk free rate
        :param t: time to expiration
        :param vol: volatility
        '''
        d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)

        return self.N(d1) - 1.0

    def gamma(self,S, K, r, t, vol):
        '''
        Black-Scholes Gamma.
        Second partial derivative of the option value with respect
        to the change in the underlying stock price. Gamma measures movements in delta
        or the convexity in the value of the option with respect to the underlying.

        :param S: underlying stock price
        :param K: strike price
        :param r: risk free rate
        :param t: time to expiration
        :param vol: volatility
        '''
        d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)

        return self.phi(d1) / (S * vol * np.sqrt(t))

    def vega(self,S, K, r, t, vol):
        '''
        Black-Scholes Vega. (Returns percentage)
        Partial derivative of the option value with respect to
        the change in the volatility of the underling. Vega measures
        how the option price moves with respect to the volatility of the underlying.

        :param S: underlying stock price
        :param K: strike price
        :param r: risk free rate
        :param t: time to expiration
        :param vol: volatility
        '''
        d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
        return S * self.phi(d1) * np.sqrt(t) / 100

    def call_theta(self,S, K, r, t, vol):
        '''
        Black-Scholes Call Theta(Annualised).
        Partial derivative of the option value with respect to the change in time.
        Shows the decay of value of option as time passes.

        :param S: underlying stock price
        :param K: strike price
        :param r: risk free rate
        :param t: time to expiration
        :param vol: volatility
        '''

        d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
        d2 = d1 - (vol * np.sqrt(t))

        theta = (-S * self.phi(d1) * vol) / (2 * np.sqrt(t)) - (r * K * np.exp(-r * t) * self.N(d2))
        return theta / 365.0

    def put_theta(self,S, K, r, t, vol):
        '''
        Black-Scholes Put Theta(Annualised).
        Partial derivative of the option value with respect to the change in time.
        Shows the decay of value of option as time passes.

        :param S: underlying stock price
        :param K: strike price
        :param r: risk free rate
        :param t: time to expiration
        :param vol: volatility
        '''

        d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
        d2 = d1 - (vol * np.sqrt(t))

        theta = (-S * self.phi(d1) * vol) / (2 * np.sqrt(t)) + (r * K * np.exp(-r * t) * self.N(-d2))
        return theta / 365.0

    def call_rho(self,S, K, r, t, vol):
        '''
        Black-Scholes Call Rho.(Returns Percentage)
        Partial derivative of the option value with respect to change in the risk-free interest rate.
        Rho measures how the option value changes as the interest rate changes.

        :param S: underlying stock price
        :param K: strike price
        :param r: risk free rate
        :param t: time to expiration
        :param vol: volatility
        '''
        d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2) * t)
        d2 = d1 - (vol * np.sqrt(t))

        rho = K * t * np.exp(-r * t) * self.N(d2)
        return rho / 100.0

    def put_rho(self,S, K, r, t, vol):
        '''
        Black-Scholes Put Rho.(Returns Percentage)
        Partial derivative of the option value with respect to change in the risk-free interest rate.
        Rho measures how the option value changes as the interest rate changes.

        :param S: underlying stock price
        :param K: strike price
        :param r: risk free rate
        :param t: time to expiration
        :param vol: volatility
        '''
        d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2) * t)
        d2 = d1 - (vol * np.sqrt(t))

        rho = -K * t * np.exp(-r * t) * self.N(-d2)
        return rho / 100.0

    def replace_iv(self,current_date, calls_data):
        try:
            iv = calls_data[(calls_data['temp_date'] < current_date) & (calls_data['iv'] > 0)]['iv'].iloc[0]
        except:
            iv = 0
        return iv


    def get_data(self):
        try:
            session = requests.Session()
            response = session.get(self.url, headers=self.headers).json()
            rawdata = pd.DataFrame(response)
            raw_op_current = pd.DataFrame(rawdata['filtered']['data']).fillna(0)
            raw_op_all = pd.DataFrame(rawdata['records']['data']).fillna(0)
            return raw_op_all,rawdata,"SUCCESS"
        except Exception as e:
            return [],[],"FAIL"

    def get_expiry_dates(self):
        raw_options, rawdata, status = self.get_data()
        if status != "SUCCESS":
            return [],"FAIL"
        return rawdata['records']['expiryDates'],"SUCCESS"

    def get_curated_data(self):
        try:
            raw_options,rawdata,status = self.get_data()
            if status != "SUCCESS":
                return [],[],"FAIL"
            todays_date = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d")
            call_options = []
            put_options = []
            for i in range(0, len(raw_options)):

                call_oi = call_oi_change = call_ltp = call_volume = call_underlying = call_strike = call_iv = call_expiry_date = call_lt_change = put_expiry_date = put_iv = put_oi = put_oi_change = put_ltp = put_strike = put_volume = put_lt_change = put_underlying = 0
                strike_price = raw_options['strikePrice'][i]
                if raw_options['CE'][i] == 0:
                    call_oi = call_oi_change = 0
                else:
                    call_oi = raw_options['CE'][i]['openInterest']
                    call_oi_change = raw_options['CE'][i]['changeinOpenInterest']
                    call_ltp = raw_options['CE'][i]['lastPrice']
                    call_volume = raw_options['CE'][i]['totalTradedVolume']
                    call_iv = raw_options['CE'][i]['impliedVolatility']
                    call_expiry_date = raw_options['CE'][i]['expiryDate']
                    call_lt_change = raw_options['CE'][i]['change']
                    call_underlying = raw_options['CE'][i]['underlyingValue']

                if raw_options['PE'][i] == 0:
                    put_oi = put_oi_change = 0
                else:
                    put_oi = raw_options['PE'][i]['openInterest']
                    put_oi_change = raw_options['PE'][i]['changeinOpenInterest']
                    put_ltp = raw_options['PE'][i]['lastPrice']
                    put_volume = raw_options['PE'][i]['totalTradedVolume']
                    put_iv = raw_options['PE'][i]['impliedVolatility']
                    put_expiry_date = raw_options['PE'][i]['expiryDate']
                    put_lt_change = raw_options['PE'][i]['change']
                    put_underlying = raw_options['PE'][i]['underlyingValue']

                call_options_data = {
                    'oi': call_oi, 'oi_change': call_oi_change, 'ltp': call_ltp,
                    'volume': call_volume, 'strike_price': strike_price, 'iv': call_iv,
                    'expiry': call_expiry_date, 'ltp_net_chng': call_lt_change, 'underlying_value': call_underlying
                }

                put_options_data = {
                    'oi': put_oi, 'oi_change': put_oi_change, 'ltp': put_ltp,
                    'volume': put_volume, 'strike_price': strike_price, 'iv': put_iv,
                    'expiry': put_expiry_date, 'ltp_net_chng': put_lt_change, 'underlying_value': put_underlying
                }
                call_options.append(call_options_data)
                put_options.append(put_options_data)

            put_option_chain = pd.DataFrame(put_options)
            call_option_chain = pd.DataFrame(call_options)

            put_option_chain = put_option_chain[put_option_chain['ltp'] != 0]
            call_option_chain = call_option_chain[call_option_chain['ltp'] != 0]

            put_option_chain['today_date'] = todays_date
            call_option_chain['today_date'] = todays_date

            put_option_chain['days_to_expiry'] = (
                        pd.to_datetime(put_option_chain['expiry']) - pd.to_datetime(put_option_chain['today_date'])).dt.days
            call_option_chain['days_to_expiry'] = (pd.to_datetime(call_option_chain['expiry']) - pd.to_datetime(
                call_option_chain['today_date'])).dt.days

            put_option_chain.drop(columns=['today_date'], inplace=True)
            call_option_chain.drop(columns=['today_date'], inplace=True)

            put_option_chain['underlying'] = 'NIFTY'
            call_option_chain['underlying'] = 'NIFTY'

            timestamp = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

            put_option_chain['timestamp'] = timestamp
            call_option_chain['timestamp'] = timestamp

            put_option_chain['timestamp_create'] = timestamp
            call_option_chain['timestamp_create'] = timestamp

            put_option_chain['contract'] = "NIFTY-" + put_option_chain['expiry'].str.replace("-", "") + "-PE-" + \
                                           put_option_chain['strike_price'].astype(str)
            call_option_chain['contract'] = "NIFTY-" + call_option_chain['expiry'].str.replace("-", "") + "-CE-" + \
                                            call_option_chain['strike_price'].astype(str)

            put_option_chain['contract'] = put_option_chain['contract'].str.upper()
            call_option_chain['contract'] = call_option_chain['contract'].str.upper()

            put_option_chain['contract_type'] = 'PE'
            call_option_chain['contract_type'] = 'CE'

            call_option_chain['temp_date'] = pd.to_datetime(call_option_chain['expiry'])
            put_option_chain['temp_date'] = pd.to_datetime(put_option_chain['expiry'])

            call_option_chain = call_option_chain.sort_values(by='temp_date', ascending=False)
            put_option_chain = put_option_chain.sort_values(by='temp_date', ascending=False)

            new_ivs = []
            for _, i in call_option_chain.iterrows():
                if i['iv'] == 0:
                    iv = self.replace_iv(i['iv'], call_option_chain)
                else:
                    iv = i['iv']
                new_ivs.append(iv)

            call_option_chain['iv'] = new_ivs

            new_ivs = []
            for _, i in put_option_chain.iterrows():
                if i['iv'] == 0:
                    iv = self.replace_iv(i['iv'], put_option_chain)
                else:
                    iv = i['iv']
                new_ivs.append(iv)

            put_option_chain['iv'] = new_ivs

            call_option_chain['delta'] = call_option_chain.apply(
                lambda x: self.call_delta(x['underlying_value'], x['strike_price'], 0.1,
                                     x['days_to_expiry'], x['iv']), axis=1)
            call_option_chain['gamma'] = call_option_chain.apply(
                lambda x: self.gamma(x['underlying_value'], x['strike_price'], 0.1,
                                x['days_to_expiry'], x['iv']), axis=1)

            call_option_chain['vega'] = call_option_chain.apply(
                lambda x: self.vega(x['underlying_value'], x['strike_price'], 0.1,
                               x['days_to_expiry'], x['iv']), axis=1)

            call_option_chain['theta'] = call_option_chain.apply(
                lambda x: self.call_theta(x['underlying_value'], x['strike_price'], 0.1,
                                     x['days_to_expiry'], x['iv']), axis=1)

            call_option_chain['rho'] = call_option_chain.apply(
                lambda x: self.call_rho(x['underlying_value'], x['strike_price'], 0.1,
                                   x['days_to_expiry'], x['iv']), axis=1)

            put_option_chain['delta'] = put_option_chain.apply(
                lambda x: self.put_delta(x['underlying_value'], x['strike_price'], 0.1,
                                    x['days_to_expiry'], x['iv']), axis=1)
            put_option_chain['gamma'] = put_option_chain.apply(
                lambda x: self.gamma(x['underlying_value'], x['strike_price'], 0.1,
                                x['days_to_expiry'], x['iv']), axis=1)

            put_option_chain['vega'] = put_option_chain.apply(lambda x: self.vega(x['underlying_value'], x['strike_price'], 0.1,
                                                                             x['days_to_expiry'], x['iv']), axis=1)

            put_option_chain['theta'] = put_option_chain.apply(
                lambda x: self.put_theta(x['underlying_value'], x['strike_price'], 0.1,
                                    x['days_to_expiry'], x['iv']), axis=1)

            put_option_chain['rho'] = put_option_chain.apply(
                lambda x: self.put_rho(x['underlying_value'], x['strike_price'], 0.1,
                                  x['days_to_expiry'], x['iv']), axis=1)

            put_option_chain.drop(columns=['underlying_value', 'oi_change', 'temp_date', 'iv'], inplace=True)
            call_option_chain.drop(columns=['underlying_value', 'oi_change', 'temp_date', 'iv'], inplace=True)

            put_option_chain['expiry'] = pd.to_datetime(put_option_chain['expiry'])
            call_option_chain['expiry'] = pd.to_datetime(call_option_chain['expiry'])

            put_option_chain['gamma'] = put_option_chain['gamma'].fillna(0.0)
            call_option_chain['gamma'] = call_option_chain['gamma'].fillna(0.0)
            return put_option_chain, call_option_chain,"SUCCESS"
        except:
            return [],[],"FAIL"

