import os
import sys
sys.path.insert(0, '/opt/python/pip_modules')

# from matplotlib.pyplot import title
import mplfinance as mpf
import matplotlib.ticker as ticker
import requests

from datetime import datetime
from datetime import timedelta
import simplejson as json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import pandas as pd

from math import log, floor

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

import boto3
s3 = boto3.resource('s3')

# Environment Variables
ENV_VARS = {
    'BUCKET_NAME': ''
}

def format_price(number):
    units = ['', 'K', 'M', 'B', 'T']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])

def create_graph_image(raw_data: dict) -> str:
    price_decimals = '%.4f'

    formatted_data = []
    for item in raw_data:
        entry = {}
        entry['date'] = datetime.fromtimestamp(int(item['timestamp'])/1000)
        entry['open'] = float(item['openUsd'])
        entry['high'] = float(item['highUsd'])
        entry['low'] = float(item['lowUsd'])
        entry['close'] = float(item['closeUsd'])
        entry['volume'] = float(item['volumeUsd'])
        formatted_data.append(entry)

    df = pd.DataFrame(formatted_data)
    df.index = pd.DatetimeIndex(df['date'])

    colours = {
        'line': '#004475',
        'up': '#004475',
        'down': '#92C8F0',
        'edge_up': '#004475',
        'edge_down': '#92C8F0',
        'wick_up': '#004475',
        'wick_down': '#92C8F0',
        'face': '#E7F1F8',
        'edge': '#E7F1F8',
        'fig': '#E7F1F8',
        'grid': '#97C0DE',
    }

    img_path = f"/tmp/output-crow-finance.png"

    kwargs = dict(type='candle', volume=True, linecolor=colours['line'], returnfig=True, datetime_format='%H:%M', xrotation=0)
    mc = mpf.make_marketcolors(up=colours['up'], down=colours['down'], volume='inherit', 
                                edge={'up': colours['edge_up'], 'down': colours['edge_down']}, 
                                wick={'up': colours['wick_up'], 'down': colours['wick_down']})

    s = mpf.make_mpf_style(base_mpf_style='starsandstripes', marketcolors=mc, y_on_right=True,
                           facecolor=colours['face'], edgecolor=colours['edge'], figcolor=colours['fig'], 
                           gridcolor=colours['grid'], gridstyle='--')

    fig, axlist = mpf.plot(df, **kwargs, style=s)

    for ax in axlist:
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(price_decimals))

    fig.savefig(fname=img_path, bbox_inches='tight')

    return img_path


def lambda_handler(event, context):
    try:
        logger.info(f'[ INIT - EVENT ] {json.dumps(event)}')

        logger.info('[ INIT ] Validating environment variables')
        for var in ENV_VARS:
            ENV_VARS[var] = os.environ.get(var)
            if ENV_VARS[var] is None:
                raise NameError('Unable to retrieve one or more environment variables')
                
        crow_token_address = '0x285c3329930a3fd3C7c14bC041d3E50e165b1517'
        crow_usd_pair_address = '0x82E623AA112B03388A153D51142e5F9eA7EcE258'
        crow_cro_pair_address = '0xCd693F158865D071f100444c7F3b96e7463bAe8d'
        dexscreen_api_base_url = 'https://c4.dexscreen.com'
        cronos_api_base_url = 'https://cronos.crypto.org/explorer/api'

        bucket_name = ENV_VARS['BUCKET_NAME']
        
        crow_cro_price = ''
        crow_cro_24h_txns = '' 
        crow_cro_24h_vol = ''
        crow_cro_24h_chng = ''
        crow_cro_24h_lqdty = ''
        
        crow_usdc_price = ''
        crow_usdc_24h_txns = '' 
        crow_usdc_24h_vol = ''
        crow_usdc_24h_chng = ''
        crow_usdc_24h_lqdty = ''
        
        pairs_response = requests.get(f'{dexscreen_api_base_url}/u/search/pairs?q=crow')

        for pair in pairs_response.json()['pairs']:
            if pair['baseToken']['address'] == crow_token_address:
                if pair['quoteTokenSymbol'] == 'WCRO':
                    crow_cro_price = f"${pair['priceUsd']}"
                    crow_cro_24h_txns = pair['h24Txns']
                    crow_cro_24h_vol = "${:,.0f}".format(int(pair['h24VolumeUsd']))
                    crow_cro_24h_chng = pair['h24PriceChange']
                    crow_cro_24h_lqdty = "${:,.0f}".format(int(pair['liquidity']))
                if pair['quoteTokenSymbol'] == 'USDC':
                    crow_usdc_price = f"${pair['priceUsd']}"
                    crow_usdc_24h_txns = pair['h24Txns']
                    crow_usdc_24h_vol = "${:,.0f}".format(int(pair['h24VolumeUsd']))
                    crow_usdc_24h_chng = pair['h24PriceChange']
                    crow_usdc_24h_lqdty = "${:,.0f}".format(int(pair['liquidity']))

        fetch_holders = True
        page_number = 1
        holders_per_page = 1000
        crow_holders = 0
        while fetch_holders:
            holders_response = requests.get(f'{cronos_api_base_url}?module=token&action=getTokenHolders&contractaddress={crow_token_address}&page={page_number}&offset={holders_per_page}')

            for holder in holders_response.json()['result']:
                crow_holders += 1
            if len(holders_response.json()['result']) < holders_per_page:
                fetch_holders = False
            else:
                page_number += 1

        token_supply_response = requests.get(f'{cronos_api_base_url}?module=stats&action=tokensupply&contractaddress={crow_token_address}')
        token_supply = token_supply_response.json()['result']
        circulating_supply = format_price(int(token_supply.split(token_supply[-18:])[0]))
        market_cap = format_price(int(token_supply.split(token_supply[-18:])[0]) * float(crow_cro_price.split('$')[1]))

        now = datetime.utcnow()
        now_timestamp = now.timestamp() * 1000
        one_hour_ago = now - timedelta(hours=1)
        one_hour_ago_timestamp = one_hour_ago.timestamp() * 1000

        one_hour_chart_cro_response = requests.get(f'https://c7.dexscreen.com/u/chart/bars/cronos/{crow_cro_pair_address}?from={one_hour_ago_timestamp}&to={now_timestamp}&res=5&cb=12')
        open_cro_price = float(one_hour_chart_cro_response.json()['bars'][0]['openUsd'])
        close_cro_price = float(one_hour_chart_cro_response.json()['bars'][-1]['closeUsd'])
        print(f'{open_cro_price} : {close_cro_price}')
        one_hour_cro_pct_change = round(float(((close_cro_price - open_cro_price) * 100) / open_cro_price), 2)
        print(one_hour_cro_pct_change)

        one_hour_chart_usd_response = requests.get(f'https://c7.dexscreen.com/u/chart/bars/cronos/{crow_usd_pair_address}?from={one_hour_ago_timestamp}&to={now_timestamp}&res=5&cb=12')
        open_usd_price = float(one_hour_chart_usd_response.json()['bars'][0]['openUsd'])
        close_usd_price = float(one_hour_chart_usd_response.json()['bars'][-1]['closeUsd'])
        print(f'{open_usd_price} : {close_usd_price}')
        one_hour_usd_pct_change = round(float(((close_usd_price - open_usd_price) * 100) / open_usd_price), 2)
        print(one_hour_usd_pct_change)

        price_info_text = f'''Current price information with 1 hour chart\n\nName: *Crow Token*\nSymbol: *CROW*\nMarket Cap: *{market_cap}*\nTotal Supply: *1B*\nCirculating Supply: *{circulating_supply}*\nTotal Holders: *{crow_holders}*\n\nTrading pairs\n\n*CROW/CRO*\nCROW Price (USD): *{crow_cro_price}*\n24H Transactions: *{crow_cro_24h_txns}*\n24H Volume (USD): *{crow_cro_24h_vol}*\n24H Price Change: *{crow_cro_24h_chng}%*\n1H Price Change: *{one_hour_cro_pct_change}%*\nLiquidity: *{crow_cro_24h_lqdty}*\n\n*CROW/USDC*\nCROW Price (USD): *{crow_usdc_price}*\n24H Transactions: *{crow_usdc_24h_txns}*\n24H Volume (USD): *{crow_usdc_24h_vol}*\n24H Price Change: *{crow_usdc_24h_chng}%*\n1H Price Change: *{one_hour_usd_pct_change}%*\nLiquidity: *{crow_usdc_24h_lqdty}*'''

        temp_file_path = f"/tmp/crow-finance.txt"
        with open(temp_file_path, 'w') as f:
            f.write(price_info_text)
        s3.meta.client.upload_file(temp_file_path, bucket_name, "crow-finance.txt")
        logger.info(f"[ PRICE DATA ] Fetching price data for token crow-finance complete")

        yesterday = now - timedelta(days=1)
        yesterday_timestamp = yesterday.timestamp() * 1000

        chart_response = requests.get(f'https://c7.dexscreen.com/u/chart/bars/cronos/{crow_cro_pair_address}?from={yesterday_timestamp}&to={now_timestamp}&res=60&cb=24')
        ohlc_file = create_graph_image(chart_response.json()['bars'])
        s3.meta.client.upload_file(ohlc_file, bucket_name, "crow-finance.png")
        logger.info(f"[ RENDER ] Render for token Crow Finance complete")

        seven_days_ago = now - timedelta(days=7)
        seven_days_ago_timestamp = seven_days_ago.timestamp() * 1000

        fourh_chart_response = requests.get(f'https://c7.dexscreen.com/u/chart/bars/cronos/{crow_cro_pair_address}?from={seven_days_ago_timestamp}&to={now_timestamp}&res=240&cb=168')
        fourh_ohlc_file = create_graph_image(fourh_chart_response.json()['bars'])
        s3.meta.client.upload_file(fourh_ohlc_file, bucket_name, "crow-finance-4h.png")
        logger.info(f"[ RENDER ] Render for token Crow Finance 4H complete")

        four_weeks_ago = now - timedelta(weeks=4)
        four_weeks_ago_timestamp = four_weeks_ago.timestamp() * 1000

        oned_chart_response = requests.get(f'https://c7.dexscreen.com/u/chart/bars/cronos/{crow_cro_pair_address}?from={four_weeks_ago_timestamp}&to={now_timestamp}&res=1440&cb=30')
        oned_ohlc_file = create_graph_image(oned_chart_response.json()['bars'])
        s3.meta.client.upload_file(oned_ohlc_file, bucket_name, "crow-finance-1d.png")
        logger.info(f"[ RENDER ] Render for token Crow Finance 1D complete")

    except Exception as error:
        logger.error(f'[ FAIL ] Unhandled event: {error}')
        return

    return