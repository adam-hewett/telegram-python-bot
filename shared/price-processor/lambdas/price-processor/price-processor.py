import os
import sys
sys.path.insert(0, '/opt/python/pip_modules')

# from matplotlib.pyplot import title
import mplfinance as mpf
import matplotlib.ticker as ticker
import requests

from bs4 import BeautifulSoup
import cloudscraper

from datetime import datetime
import simplejson as json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import pandas as pd

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

import boto3
s3 = boto3.resource('s3')

# Environment Variables
ENV_VARS = {
    'BUCKET_NAME': ''
}

MANAGED_TOKENS = [
            {
                'token_name': 'only-1-token',
                'token_full_name': 'Only 1 Token',
                'token_symbol': 'O1T',
                'vs_currency': 'usd',
                'chart_days': '1',
                'contract_address': '0xBB994E80E2eDc45dCe9065bda73ADc7E9337b64F',
                'lp_contract_address': '0x98eeda2abe0a09c6111182c210907d3bf6098efe',
                'price_decimals': '%.0f'
            },
            {
                'token_name': 'fatcake',
                'token_full_name': 'Fat Cake',
                'token_symbol': 'FATCAKE',
                'vs_currency': 'usd',
                'chart_days': '1',
                'contract_address': '0xb7dba4c673bedb174dc3ff7ec65d17c863d39b16',
                'lp_contract_address': '0x6612879d031846723Ecf7322AfB4f3a97A045dc2',
                'price_decimals': '%.8f'
            }
        ]

def create_graph_image(token_info: dict) -> str:
    token_name = token_info['token_name']
    vc_currency = token_info['vs_currency']
    chart_days = token_info['chart_days']
    price_decimals = token_info['price_decimals']
    
    stock_price_url = f"https://api.coingecko.com/api/v3/coins/{token_name}/ohlc?vs_currency={vc_currency}&days={chart_days}"
    source_code = requests.get(stock_price_url)

    raw_data = json.loads(source_code.text)

    formatted_data = []
    for item in raw_data:
        entry = {}
        entry['date'] = datetime.fromtimestamp(int(item[0])/1000)
        entry['open'] = item[1]
        entry['high'] = item[2]
        entry['low'] = item[3]
        entry['close'] = item[4]
        formatted_data.append(entry)

    df = pd.DataFrame(formatted_data)
    df.index = pd.DatetimeIndex(df['date'])

    img_path = f"/tmp/output-{token_info['token_name']}.png"

    kwargs = dict(type='line', linecolor='#22c56e', returnfig=True, datetime_format='%H:%M', xrotation=0)
    mc = mpf.make_marketcolors(up='g', down='r', edge={
                               'up': 'g', 'down': 'r'}, wick={'up': 'g', 'down': 'r'})

    s = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc, y_on_right=True,
                           facecolor='#17141e', edgecolor='#322f38', figcolor='#17141e', gridcolor='#322f38', gridstyle='--')

    fig, axlist = mpf.plot(df, **kwargs, style=s)

    for ax in axlist:
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(price_decimals))

    fig.savefig(fname=img_path, bbox_inches='tight')

    return img_path


def fetch_holders(contract_address: str) -> str:
    try:
        scraper = cloudscraper.create_scraper()
        req = scraper.get(f'https://bscscan.com/token/{contract_address}').text
        soup = BeautifulSoup(req, 'html.parser')
        div = soup.find_all('div', class_='mr-3')
        holdersResponse = div[0].get_text().split(' ')[0]
        return holdersResponse
    except Exception as error:
        logger.error(f'Error fetching holders: {error}')
        return 'an error occurred'


def fetch_lp_holders(lp_contract_address: str) -> str:
    try:
        scraper = cloudscraper.create_scraper()
        lp_req = scraper.get(f'https://bscscan.com/token/{lp_contract_address}').text
        lp_soup = BeautifulSoup(lp_req, 'html.parser')
        lp_div = lp_soup.find_all('div', class_='mr-3')
        lp_holders_response = lp_div[0].get_text().split(' ')[0]
        return lp_holders_response
    except Exception as error:
        logger.error(f'Error fetching lp holders: {error}')
        return 'an error occurred'


def get_liquidity_tokens(lp_contract_address: str, token_symbol: str):
    try:
        scraper = cloudscraper.create_scraper()
        req = scraper.get(f'https://bscscan.com/address/{lp_contract_address}').text
        soup = BeautifulSoup(req, "html.parser")
        liq_spans = soup.find_all("span", class_="list-amount link-hover__item hash-tag hash-tag--md text-truncate")
        liq_tokens = {}
        for span in liq_spans:
            if span.text.split(' ')[1] == 'WBNB':
                liq_tokens['WBNB'] = span.text.split(' ')[0]
            if span.text.split(' ')[1] == token_symbol:
                liq_tokens[token_symbol] = span.text.split(' ')[0]
        return liq_tokens
    except Exception as error:
        logger.error(f'Error fetching LP tokens: {error}')
        return 'an error occurred'


def get_price_info(token_info) -> str:
    try:
        token = token_info['token_name']
        vs_currency = token_info['vs_currency']
        token_name = token_info['token_name']
        token_symbol = token_info['token_symbol']
        lp_contract_address = token_info['lp_contract_address']
        contract_address = token_info['contract_address']

        price_response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={token}%2Cbinancecoin&vs_currencies={vs_currency}&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true')
        price_data = price_response.json()
        token_price = "${:,.0f}".format(price_data[token][vs_currency])
        token_change = int(price_data[token]['usd_24h_change'])
        token_vol = "${:,.0f}".format(price_data[token]['usd_24h_vol'])

        get_marketcap = float((price_data[token][vs_currency]) * 1)
        marketcap = locale.currency( get_marketcap, grouping=True ).split('.')[0]

        bnb_price = locale.currency(price_data['binancecoin']['usd'], grouping=True)
        bnb_change = int(price_data['binancecoin']['usd_24h_change'])

        holders = fetch_holders(contract_address)
        lp_holders = fetch_lp_holders(lp_contract_address)
        liq_tokens = get_liquidity_tokens(lp_contract_address, token_symbol)

        print(liq_tokens['WBNB'])

        bnb_liq_value = float(liq_tokens['WBNB']) * float(price_data['binancecoin'][vs_currency])
        bnb_liq_dlr_value = locale.currency( bnb_liq_value, grouping=True )
        token_liq_value = float(liq_tokens[token_symbol]) * float(price_data[token][vs_currency])
        token_liq_dlr_value = locale.currency( token_liq_value, grouping=True )
        liq_total = locale.currency( float(bnb_liq_value) + float(token_liq_value), grouping=True )

        bnb_token_value = (float(price_data[token][vs_currency]) / float(price_data['binancecoin'][vs_currency]) * 0.010753)
        bnb_token_dlr_value = locale.currency( bnb_token_value, grouping=True ).split('$')[1]

        token_bnb_value = (1 / (float(price_data[token][vs_currency]) / float(price_data['binancecoin'][vs_currency])))
        token_bnb_dlr_value = "${:,.8f}".format( token_bnb_value, grouping=True ).split('$')[1]
        
        resp_msg = f'''Current price information\n\nName: *{token_name}*\nSymbol: *{token_symbol}*\n\n{token_symbol} Price: *{token_price} ({token_change}%) 24H*\nMarket Cap: *{marketcap}*\n24H Volume: *{token_vol}*\nHolders: *{holders.strip()}*\n\nLiquidity Total: *{liq_total}*\nLiquidity {token_symbol} Qty: *{liq_tokens[token_symbol]}*\nLiquidity {token_symbol} Value: *{token_liq_dlr_value}*\nLiquidity BNB Qty: *{liq_tokens['WBNB']}*\nLiquidity BNB Value: *{bnb_liq_dlr_value}*\nLP Holders: *{lp_holders.strip()}*\n\nBNB Price: *{bnb_price} ({bnb_change}%) 24H*\n\n1 BNB = *{token_bnb_dlr_value} {token_symbol}*\n{bnb_token_dlr_value} BNB = 1% {token_symbol} Supply'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'prices\' command: {error}')
        return 'Sorry, an error occurred processing your request, wait a few seconds and try again.'


def lambda_handler(event, context):
    try:
        logger.info(f'[ INIT - EVENT ] {json.dumps(event)}')

        logger.info('[ INIT ] Validating environment variables')
        for var in ENV_VARS:
            ENV_VARS[var] = os.environ.get(var)
            if ENV_VARS[var] is None:
                raise NameError('Unable to retrieve one or more environment variables')

        bucket_name = ENV_VARS['BUCKET_NAME']

        for token in MANAGED_TOKENS:
            logger.info(f"[ RENDER ] Rendering graph for token {token['token_name']}")
            img_path = create_graph_image(token)
            s3.meta.client.upload_file(img_path, bucket_name, f"{token['token_name']}.png")
            logger.info(f"[ RENDER ] Render for token {token['token_name']} complete")

            logger.info(f"[ PRICE DATA ] Fetching price data for token {token['token_name']}")
            price_info_text = get_price_info(token)
            temp_file_path = f"/tmp/{token['token_name']}.txt"
            with open(temp_file_path, 'w') as f:
                f.write(price_info_text)
            s3.meta.client.upload_file(temp_file_path, bucket_name, f"{token['token_name']}.txt")
            logger.info(f"[ PRICE DATA ] Fetching price data for token {token['token_name']} complete")

    except Exception as error:
        logger.error(f'[ FAIL ] Unhandled event: {error}')
        return

    return