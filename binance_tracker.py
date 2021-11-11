import configparser

from binance.client import Client
from binance.spot import Spot

from pprint import pprint
from datetime import datetime

from forex_python.converter import CurrencyRates

from ocry import ocry

#import httplib2

#http = httplib2.Http()
	
def crypto_tracker():
	# Loading keys from config file
	config = configparser.ConfigParser()
	config.read_file(open('secret1.cfg'))
	actual_api_key = config.get('BINANCE', 'ACTUAL_API_KEY')
	actual_secret_key = config.get('BINANCE', 'ACTUAL_SECRET_KEY')

	base_url='https://api.binance.com'

	limit_usage = Spot(actual_api_key, actual_secret_key, base_url=base_url, show_limit_usage=True)

	client = Client(actual_api_key, actual_secret_key)
	client.API_URL = base_url

	pprint(limit_usage.time())

	#symbols = ["DOGEUSDT", "BTCUSDT", "ETHUSDT", "TRXUSDT", "EOSUSD", "LTCUSD", "XRPUSDT"]
	symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "EOSUSD", "LTCUSD", "TRXUSDT", "XLMUSDT", "ZRXUSDT", "DOGEUSDT"]

	#response, content = http.request('https://api.binance.com/api/v3/ticker/price')
	#pprint(content)

	#pprint(client.futures_symbol_ticker())
	#pprint(client.futures_coin_symbol_ticker())

	#-----Filter-----

	#pprint(client.futures_symbol_ticker())
	currencies = client.futures_symbol_ticker()

	for i in range(len(currencies)):
		if(currencies[i]['symbol'] in symbols):
			ts = int(str(currencies[i]['time'])[:-3])
			time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			crypto = currencies[i]['symbol'][:-4]
			price = currencies[i]['price']
			
			print(time, " --- ", crypto, " --- ", price, " US Dollars --- ", usd_to_ron(float(price)), " --- RON")

def usd_to_ron(usdValue):
	c = CurrencyRates()
	return round(c.convert('USD', 'RON', usdValue), 2)

crypto_tracker()	

oc = ocry()
oc.setdoge(60)
print(oc.getdoge())


