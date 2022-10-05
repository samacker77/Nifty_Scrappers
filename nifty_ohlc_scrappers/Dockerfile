FROM python:3

WORKDIR nifty_ohlc_scrappers

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "nifty_ohlc_4pm_ist/start_app.py" ]