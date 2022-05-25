import configparser
import time
import requests
import datetime
import csv

from os.path import exists

from binance.client import Client
from binance.spot import Spot

from pprint import pprint

from forex_python.converter import CurrencyRates

day_details = {
	"day" : 1,
	"usd_to_ron" : 1
}

stats = {
	"btc_time_1m" : 1,
	"btc_price_1m" : 1,
	"btc_percentage_1m" : 1,
	"btc_price_diff_1m" : 1,
	"mana_time_1m" : 1,
	"mana_price_1m" : 1,
	"mana_percentage_1m" : 1,
	"mana_price_diff_1m" : 1
}

settings = {
	"btc_perc_init" : True,
	"mana_perc_init" : True
}

def crypto_tracker():
	# Loading keys from config file
	config = configparser.ConfigParser()
	config.read_file(open('settings.cfg'))
	actual_api_key = config.get('BINANCE', 'ACTUAL_API_KEY')
	actual_secret_key = config.get('BINANCE', 'ACTUAL_SECRET_KEY')

	base_url='https://api.binance.com'

	limit_usage = Spot(actual_api_key, actual_secret_key, base_url=base_url, show_limit_usage=True)

	client = Client(actual_api_key, actual_secret_key)
	client.API_URL = base_url

	print("\nCalls per 1 minute:", limit_usage.time()['limit_usage']['x-mbx-used-weight-1m'])

	symbols = ["BTCUSDT", "MANAUSDT", "ETHUSDT"]#, "SOLUSDT", "LTCUSDT"]#, "XRPUSDT", "EOSUSDT", "TRXUSDT", "XLMUSDT", "ZRXUSDT", "DOGEUSDT", "XTZUSDT"]

	# response, content = urllib.request('https://api.binance.com/api/v3/ticker/price')
	# pprint(content)

	# pprint(client.futures_symbol_ticker())
	# pprint(client.futures_coin_symbol_ticker()[1])

	#-----Filter-----

	# pprint(client.futures_symbol_ticker())
	currencies = client.futures_symbol_ticker()

	total = 0
	investit = 130

	for i in range(len(currencies)):
		if(currencies[i]['symbol'] in symbols):
			ts = int(str(currencies[i]['time'])[:-3])
			normal_time = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			crypto = currencies[i]['symbol'][:-4]
			price = currencies[i]['price']
			
			pret_in_moneda_ron = round(usd_to_ron(float(price)), 2)
			
			if(crypto == "BTC"):
				x = 0.00036704
			if(crypto == "MANA"):
				x = 14.53288219
			if(crypto == "ETH"):
				x = 0.00311631
			
			if(crypto == "BTC"):
				toPrint = []
				toPrint.append(normal_time)
				toPrint.append(crypto)
				toPrint.append(price)
				saveToCSV(toPrint)
				print(toPrint)
			
			print(normal_time, " --- ", crypto, " --- ", price, " US Dollars --- ", pret_in_moneda_ron, " --- RON --- ", round(pret_in_moneda_ron * x, 2), " --- detinut")		
			
			total = total + round(pret_in_moneda_ron * x, 2)
			
			if(crypto == "BTC"):
				if(settings['btc_perc_init']):
					settings['btc_perc_init'] = False
					stats['btc_time_1m'] = ts
					stats['btc_price_1m'] = float(price)
				
				if(ts - stats['btc_time_1m'] >= 60):
					stats['btc_time_1m'] = ts
					stats['btc_percentage_1m'] = round(((100*float(price))/stats['btc_price_1m'])-100, 4)
					stats['btc_price_diff_1m'] = stats['btc_price_1m'] * (stats['btc_percentage_1m']/100)
					stats['btc_price_1m'] = float(price)
					print("BTC - Percentage price difference: ", stats['btc_percentage_1m'], " %")
					print("BTC - Price difference in dollars: ", round(stats['btc_price_diff_1m'], 2))
				
			if(crypto == "MANA"):
				if(settings['mana_perc_init']):
					settings['mana_perc_init'] = False
					stats['mana_time_1m'] = ts
					stats['mana_price_1m'] = float(price)
				
				if(ts - stats['mana_time_1m'] >= 60):
					stats['mana_time_1m'] = ts
					stats['mana_percentage_1m'] = round(((100*float(price))/stats['mana_price_1m'])-100, 4)
					stats['mana_price_diff_1m'] = stats['mana_price_1m'] * (stats['mana_percentage_1m']/100)
					stats['mana_price_1m'] = float(price)
					print("MANA - Percentage price difference: ", stats['mana_percentage_1m'], " %")
					print("MANA - Price difference in dollars: ", round(stats['mana_price_diff_1m'], 2))
	
	profit = round(total - investit, 2)
	print("investit: ", investit, "\ntotal: ", total, "\nprofit: ", profit)
	
def usd_to_ron(usdValue):
	return usdValue*day_details['usd_to_ron']

def get_currency_rate():

	config = configparser.ConfigParser()
	config.read_file(open('settings.cfg'))
	api_key = config.get('EXCHANGERATE', 'API_KEY')
	url = "https://v6.exchangerate-api.com/v6/" + api_key + "/latest/USD"
	
	response = requests.get(url)
	data = response.json()
	
	return round(float(data['conversion_rates']['RON']), 2)

def update_rates():
	day_details['usd_to_ron'] = get_currency_rate()

def update_day():
	day_details['day'] = datetime.datetime.now().day

def saveToCSV(DatasetData):
	if exists('BTC_Dataset_HighFrequency.csv'):
		print('appended to file')
		f = open('BTC_Dataset_HighFrequency.csv', 'a', encoding='UTF8', newline='')
		writer = csv.writer(f)
		writer.writerow(DatasetData)
		f.close()
	else:
		print('created the file')
		f = open('BTC_Dataset_HighFrequency.csv', 'w', encoding='UTF8', newline='')
		writer = csv.writer(f)
		header = ['date', 'symbol', 'price']
		writer.writerow(header)
		writer.writerow(DatasetData)
		f.close()

def main():
	config = configparser.ConfigParser()
	config.read('settings.cfg')
	if(config['DETAILS']['FIRST_RUN'] == 'TRUE' or config['DETAILS']['DAY'] != str(datetime.datetime.now().day)):
	
		config['DETAILS']['FIRST_RUN'] = 'FALSE'
		config['DETAILS']['DAY'] = str(datetime.datetime.now().day)
		config['DETAILS']['USD_TO_RON'] = str(get_currency_rate())
		
		update_day()
		update_rates()
		
		with open('settings.cfg', 'w') as configfile:
			config.write(configfile)
	
	if(config['DETAILS']['FIRST_RUN'] == 'FALSE'):
		day_details['usd_to_ron'] = float(config['DETAILS']['USD_TO_RON'])
		day_details['day'] = int(config['DETAILS']['DAY'])
	
	while True:
		crypto_tracker()
		time.sleep(5)

main()