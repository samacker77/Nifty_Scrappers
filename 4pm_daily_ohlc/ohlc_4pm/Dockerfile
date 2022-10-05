FROM ubuntu:20.04
WORKDIR ohlc_4pm
COPY . .

RUN apt-get update && apt-get -y install python3 python3-dev
RUN apt-get install -y python3-pip
RUN python3 -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
CMD [ "python3", "-u", "nifty_ohlc_4pm_ist/start_app.py" ]