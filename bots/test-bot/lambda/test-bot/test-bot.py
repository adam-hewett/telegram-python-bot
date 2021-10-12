#building for O1T

import os
import sys
sys.path.insert(0, '/opt/python/pip_modules')

import simplejson as json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

import telebot
from telebot import types  # added by adam
from bs4 import BeautifulSoup
import requests
import cloudscraper

# Environment Variables
ENV_VARS = {
    'telegramApiKey': '',
    'BOT_NAME': ''
}

CONTRACT_ADDRESS = '0xBB994E80E2eDc45dCe9065bda73ADc7E9337b64F'

ERROR_MESSAGES = {
    'default': 'Sorry, an error occurred processing your request, wait a few seconds and try again.'
}

LINKS = {
    'website': 'only1token.com',
    'website_photo': 'https://i.ibb.co/QDjW41N/website.jpg',
    'lightpaper': 'only1token.medium.com/o1t-lightpaper-8729898a392e',
    'poocoin': 'https://poocoin.app/tokens/0xbb994e80e2edc45dce9065bda73adc7e9337b64f',
    'pcs': 'https://pancakeswap.finance/swap?outputCurrency=0xBB994E80E2eDc45dCe9065bda73ADc7E9337b64F',
    'rewards': 'https://trackbsc.com/earnings?token=0xBB994E80E2eDc45dCe9065bda73ADc7E9337b64F',
    'bsc': 'https://bscscan.com/token/0xbb994e80e2edc45dce9065bda73adc7e9337b64f',
    'bsc_liq': 'https://bscscan.com/address/0x98eeda2abe0a09c6111182c210907d3bf6098efe',
    'lp_holders': 'https://bscscan.com/token/0x98eeda2abe0a09c6111182c210907d3bf6098efe',
    'bscscan_photo': 'https://i.ibb.co/9HKV2VL/BSCscanv1.jpg',
    'holders_photo': 'https://i.ibb.co/2Krv4D9/photo-2021-09-17-10-10-05.jpg',
    'meme': 'https://eyes.justmoney.io/#o1t',
    'meme_photo': 'https://i.ibb.co/FbzfkNz/meme.jpg',
    'bogged': 'https://charts.bogged.finance/?token=0xbb994e80e2edc45dce9065bda73adc7e9337b64f',
    'dex': 'https://www.dextools.io/app/pancakeswap/pair-explorer/0x98eeda2abe0a09c6111182c210907d3bf6098efe',
    'guru':'https://dex.guru/token/0xbb994e80e2edc45dce9065bda73adc7e9337b64f-bsc',
    'portfolio': 'https://trackbsc.com/portfolio',
    'liquidity': 'https://dxsale.app/app/pages/dxlockview?id=0&add=0x83e4152cc57c6A0BBA8bC1F3C658c524Ee28a5f2&type=lplock&chain=BSC',
    'medium': 'https://only1token.medium.com/',
    'faq': 'https://www.reddit.com/r/only1token/comments/ocifwp/o1t_unofficial_faq_created_by_the_community_for/',
    'buy_photo': 'https://i.ibb.co/C77NwNS/PCSv2.jpg',
    'tax_photo': 'https://ibb.co/gD71qxN',
    'earnings_photo': 'https://i.ibb.co/TW0x2gN/Rewards-Tracker.jpg',
    'earnings_article': 'https://only1token.medium.com/trackbsc-com-updates-18b5a2dce22a',
    'portfolio_photo': 'https://i.ibb.co/K59pkBd/Portfolio-Tracker.jpg',
    'portfolio_article': 'https://only1token.medium.com/portfolio-tracker-updates-74878209659d'
}

SUPPORTED_COMMANDS = [
    'holders',
    'website',
    'prices',
    'earningstracker',
    'portfoliotracker',
    'buy',
    'tax',
    'slippage',
    'chart',
    'contract',
    'bscscan',
    'liquidity',
    'mediumarticles',
    'todolist',
    'faq',
    'allcommands',
    'tokenomics',
    'mememaker',
    'shillpost',
    'lp_holders'
]

EXCLUDED_COMMANDS = [
#    'prices'
    'price'
]


def fetch_holders():
    try:
        scraper = cloudscraper.create_scraper()
        req = scraper.get(LINKS['bsc']).text
        soup = BeautifulSoup(req, 'html.parser')
        div = soup.find_all('div', class_='mr-3')
        holdersResponse = div[0].get_text().split(' ')[0]
        return holdersResponse
    except Exception as error:
        logger.error(f'Error fetching holders: {error}')
        return ERROR_MESSAGES['default']


def fetch_lp_holders():
    try:
        scraper = cloudscraper.create_scraper()
        lp_req = scraper.get(LINKS['lp_holders']).text
        lp_soup = BeautifulSoup(lp_req, 'html.parser')
        lp_div = lp_soup.find_all('div', class_='mr-3')
        print(lp_div)
        lp_holders_response = lp_div[0].get_text().split(' ')[0]
        print(lp_holders_response)
        return lp_holders_response
    except Exception as error:
        logger.error(f'Error fetching lp holders: {error}')
        return ERROR_MESSAGES['default']


def fetch_holders_command():
    try:
        holders=fetch_holders()
        lp_holders=fetch_lp_holders()
        resp_msg = f'''\U0001F4B0 O1T Holders: *{holders.strip()}*\n\U00002139 All O1T holders earn 4.9% of every token transfer.\n\n\U0001F4B0 BNB/O1T LP Holders: *{lp_holders.strip()}*\n\U00002139 All BNB/O1T LP holders earn 5% of every Buy and Sell.'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error fetching holders command: {error}')
        return ERROR_MESSAGES['default']


def get_liquidity_tokens():
    try:
        scraper = cloudscraper.create_scraper()
        req = scraper.get(LINKS['bsc_liq']).text
        soup = BeautifulSoup(req, "html.parser")
        liq_spans = soup.findAll("span", class_="list-amount link-hover__item hash-tag hash-tag--md text-truncate")
        liq_tokens = {}
        for span in liq_spans:
            print(span.text)
            if span.text.split(' ')[1] == 'WBNB':
                liq_tokens['WBNB'] = span.text.split(' ')[0]
            if span.text.split(' ')[1] == 'O1T':
                liq_tokens['O1T'] = span.text.split(' ')[0]
        print(liq_tokens)
        return liq_tokens
    except Exception as error:
        logger.error(f'Error fetching LP tokens: {error}')
        return ERROR_MESSAGES['default']


def fetch_lp():
    try:
        req = requests.get(LINKS['bsc_liq'])
        soup = BeautifulSoup(req.content, "html.parser")
        div = soup.findAll("div", class_="text-right")
        lp_response = div[0].get_text().split('@')[0]
        return lp_response
    except Exception as error:
        logger.error(f'Error fetching LP: {error}')
        return ERROR_MESSAGES['default']


def website():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F30DWebsite',
                                           callback_data='website',
                                           url=LINKS['website'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Click the button below to visit our Website!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'website\' command: {error}')
        return ERROR_MESSAGES['default'], None


def prices():
    try: 
        o1t_price_response = requests.get('https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=only-1-token&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true')
        o1t_price_data = o1t_price_response.json()
        o1t_price = locale.currency( o1t_price_data['only-1-token']['usd'], grouping=True )
        o1t_change = int(o1t_price_data['only-1-token']['usd_24h_change'])
        o1t_vol = int(o1t_price_data['only-1-token']['usd_24h_vol'])
        
        bnb_price_response = requests.get('https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=binancecoin&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true')
        bnb_price_data = bnb_price_response.json()
        bnb_price = locale.currency( bnb_price_data['binancecoin']['usd'], grouping=True )
        bnb_change = int(bnb_price_data['binancecoin']['usd_24h_change'])
        
        holders=fetch_holders()
        lp_holders=fetch_lp_holders()
        
        liq_tokens = get_liquidity_tokens()
        bnb_liq_value = float(liq_tokens['WBNB']) * float(bnb_price_data['binancecoin']['usd'])
        bnb_liq_dlr_value = locale.currency( bnb_liq_value, grouping=True )
        o1t_liq_value = float(liq_tokens['O1T']) * float(o1t_price_data['only-1-token']['usd'])
        o1t_liq_dlr_value = locale.currency( o1t_liq_value, grouping=True )
        liq_total = locale.currency( float(bnb_liq_value) + float(o1t_liq_value), grouping=True )

        resp_msg = f'''Current price information\n\nName: *Only 1 Token*\n\nSymbol: *O1T*\n\nO1T Price: *{o1t_price} ({o1t_change}%) 24H*\n24H Volume: *{o1t_vol}*\nO1T Holders: *{holders.strip()}*\n\nO1T Liquidity Total: *{liq_total}*\nLiquidity O1T Qty: *{liq_tokens['O1T']}*\nLiquidity O1T Value: *{o1t_liq_dlr_value}*\nLiquidity BNB Qty: *{liq_tokens['WBNB']}*\nLiquidity BNB Value: *{bnb_liq_dlr_value}*\nLP Holders: *{lp_holders.strip()}*\n\nBNB Price: *{bnb_price} ({bnb_change}%) 24H*'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'prices\' command: {error}')
        return ERROR_MESSAGES['default']


def earningstracker():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U00002705 Click me to visit our Earnings Tracker',
                                           callback_data='earningstracker',
                                           url=LINKS['rewards'])
        markup.add(btn_a)
        resp_msg = f'''\n\U00002139Read more about our Earnings Tracker!\n{LINKS['earnings_article']}'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'earningstracker\' command: {error}')
        return ERROR_MESSAGES['default'], None


def portfoliotracker():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U00002705 Click me to visit Portfolio Tracker', callback_data='portfoliotracker', url=LINKS['portfolio'])
        markup.add(btn_a)
        resp_msg = f'''\n\U00002139Read more about our Portfolio Tracker!\n{LINKS['portfolio_article']}'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'portfolio_tracker\' command: {error}')
        return ERROR_MESSAGES['default'], None


def buy():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F95EPancakeSwap(V2)', callback_data='buy', url=LINKS['pcs'])
        markup.add(btn_a)
        resp_msg = '\U00002139 Buy Only 1 Token on PancakeSwap(V2), use at least 8% slippage.'
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'buy\' command: {error}')
        return ERROR_MESSAGES['default'], None


def tax():
    try:
        resp_msg = '\U00002139Only 1 Token has a 7% tax on every transfer.\n4.9% goes to holders\n1.9% goes to trading liquidity.\n0.2% goes to our Project Evolution fund'
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'tax\' command: {error}')
        return ERROR_MESSAGES['default']


def slippage():
    try:
        resp_msg = f'''\n\n\U00002139 Set slippage to minimum 8% on PancakeSwap.'''
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'slippage\' command: {error}')
        return ERROR_MESSAGES['default']


def chart():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_bogged = types.InlineKeyboardButton('\U0001F4CABogged', callback_data='bogged', url=LINKS['bogged'])
        btn_dex = types.InlineKeyboardButton('\U0001F308DexGuru', callback_data='guru', url=LINKS['guru'])
        btn_poocoin = types.InlineKeyboardButton('\U0001F4A9Poocoin', callback_data='poocoin', url=LINKS['poocoin'])
        markup.add(btn_bogged, btn_dex, btn_poocoin)

        resp_msg = f'''\U00002139 Click any button below and use your favorite chart!'''

        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'chart\' command: {error}')
        return ERROR_MESSAGES['default'], None


def contract():
    try:
        resp_msg = f'''\U00002139 Contract Address:\n0xbb994e80e2edc45dce9065bda73adc7e9337b64f'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'contract\' command: {error}')
        return ERROR_MESSAGES['default']


def bscscan():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F5A8BSCscan',
                                           callback_data='bscscan',
                                           url=LINKS['bsc'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Click the button below to view BSCscan!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'bscscan\' command: {error}')
        return ERROR_MESSAGES['default'], None


def liquidity():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F512Liquidity on DxSale', callback_data='liquidity', url=LINKS['liquidity'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139Click the button below. \n\U0001F512 Liquidity on DxSale!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'liquidity\' command: {error}')
        return ERROR_MESSAGES['default'], None


def mediumarticles():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F4F0Medium Articles.', callback_data='medium_articles', url=LINKS['medium'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Click the button below to check out our latest Medium Articles!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'medium_articles\' command: {error}')
        return ERROR_MESSAGES['default'], None


def todolist():
    try:
        resp_msg = f'''Every action, Every Day, Helps Yourself and the Community. We’re not digging ditches here, just a few clicks each day. Let’s Go O1T army.\n\nLets \U0001F680 to the \U0001F319 !\n\n\U000000A9CoinMarketCap:\nhttps://coinmarketcap.com/currencies/only-1-token/\n\U00002705Click GOOD\n\U00002B50Favorite (Requires Signup)\n\n\U0001F98E CoinGecko:\nhttps://www.coingecko.com/en/coins/only-1-token\n\U00002705Click GOOD\n\U00002B50Favorite (Requires Signup)\n\n\U0001F5A5 Google Search: Only 1 Token\nhttps://www.google.com/search?q=Only+1+Token\n\n\U0001F5A5DuckDuckGo Search: Only 1 Token\nhttps://duckduckgo.com/?q=Only+1+Token&va=b&t=hc&ia=web\n\n\U0001F425 Twitter: https://twitter.com/OnlyOneToken\n\U00002705Click link, Follow, Like, Retweet, and Comment\n\nhttps://t.me/only1token/12120\U0001F680Reddit:\nhttps://www.reddit.com/r/only1token/\n\U00002705Subscribe, Upvote, Comment\n\n\U0001F4F7Instagram:\nhttps://www.instagram.com/onlyonetoken/\n\U00002705Follow, Like, and Comment\n\n\U0001F3C5Coin Sniper: https://coinsniper.net/coin/143\n\U00002705Vote (Requires Signup)\n\U00002B50Favorite (Requires Signup)\n\n\U0001F5A8BSCScan: https://bscscan.com/token/0xBB994E80E2eDc45dCe9065bda73ADc7E9337b64F#comments\n\U00002705 Click link, and Comment!'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'to_do_list\' command: {error}')
        return ERROR_MESSAGES['default']


def faq():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('Frequently Asked Questions\U0001F4AC', callback_data='faq', url=LINKS['faq'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 We have summarized all questions in our FAQ on Reddit.'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'faq\' command: {error}')
        return ERROR_MESSAGES['default'], None


def allcommands():
    try:
        resp_msg = f'''\U00002139 Here are all commands!\n\n/website - Visit our Website\n/earningstracker - Track your Earned Rewards\n/portfoliotracker - Track your BSC portfolio\n/buy - Buy on PancakeSwap\n/tax - Breakdown of our Tax\n/slippage - Set Slippage on PancakeSwap\n/chart - Check our Charts\n/contract - Contract Address\n/bscscan - BscScan Page\n/holders - Holders of this Token\n/liquidity - Check Locked Liquidity\n/tokenomics - Spiderman Meme\n/mediumarticles - Current List of Medium Articles\n/shillpost - Shill Post for Sharing\n/todolist - Members To Do List\n/mememaker - Create a O1T Meme\n/faq - Frequently Asked Questions'''
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'allcommands\' command: {error}')
        return ERROR_MESSAGES['default']


def tokenomics():
    try:
        photo_url = 'https://t.me/only1token/100088'
        resp_msg = 'Awesome Tokenomics!'
        return resp_msg, photo_url
    except Exception as error:
        logger.error(
            f'Error occurred processing \'tokenomics\' command: {error}')
        return ERROR_MESSAGES['default'], None


def mememaker():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F525 Create your own O1T Meme \U0001F525',
                                           callback_data='mememaker',
                                           url=LINKS['meme'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Click the button below to Make your own Only 1 Token Meme!\n\n\U00002705 Show JustMoney.io some love for making the O1T meme generator.'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'mememaker\' command: {error}')
        return ERROR_MESSAGES['default'], None


def shillpost():
    try:
        resp_msg = f'''Only 1 Token is a brand new concept that has never been done before. A single token with 18 decimals, shared by each of its holders who are working together to make O1T the single most valuable asset in the world.\n\n\U0001F947Our Goal: Only 1 Token aims to become the most valuable fungible token, while creating tools to help make the Binance Smart Chain ecosystem more user-friendly.\n\n\U0000261DWhile most other crypto projects have trillions of tokens in circulation, we have Only 1 Token.\n\nPrice = Market Cap.\n\n\U0001F4B0Tokenomic\n7% total tax\n4.9% to holders\n1.9% liquidity pool\n0.2% project evolution fund.\n\n\U0001F48EHold to earn: 4.9% of every transfer of O1T is distributed instantly to each O1T holder’s wallet. This is known as a “reflection fee”, and is achieved through a mechanism originally developed by Reflect Finance, which has been popularized by other projects such as SafeMoon.\n\n\U0001F69CHold to farm liquidity: 5% of every buy and sell is rewarded to LP token holders from the contract reserves as long as funds are available. 25% of the supply was sent to the contract on release of O1T to provide these rewards and it is sustained by the liquidity fee on every transfer. Since 5% of every buy and sell is being rewarded to LP holders and the liquidity fee is only 1.9%, this results in a 3.1% deficit which allows the initial 25% of the supply that is in the contract to slowly decrease  as it enters circulation. Once the contract has paid enough rewards to empty the reserves, the liquidity fee can be reduced to 0%.\n\n\U0001F525Utility\n1. TrackBSC.com/earnings is free. Check what you’ve earned from reflect rewards on ANY #BSC token that offers RFI. You are also shown the liquidity adjusted price, giving you more accurate pricing.Furthermore, additional features such as viewing other wallet’s earned rewards can be unlocked by either holding $100 worth of O1T.\n\U0001F449Earnings Article: only1token.medium.com/trackbsc-com-updates-18b5a2dce22a\n\n2. TrackBSC.com/portfolio. Track your holdings, their current market price, their liquidity adjusted value and easily trade them on PancakeSwap with a press of a button! When viewing your portfolio, you can select any of your tokens and it will direct you to the info/rewards page for that token. This will facilitate a more user-friendly navigation through your portfolio and their respective reflection rewards rather than searching for each token manually. Furthermore, additional features such as viewing other wallet’s portfolio can be unlocked by either holding $60 worth of BNB-O1T in liquidity. This feature would allow users to easily check what other wallets (such as whales) are investing in and the liquidity adjusted value of each of their holdings.\n\U0001F449Portfolio Article: only1token.medium.com/portfolio-tracker-updates-74878209659d\n\n\U0001F4D1Contract Address:\n0xbb994e80e2edc45dce9065bda73adc7e9337b64f\n\n\U0001F5A8BSCscan:\nbscscan.com/token/0xbb994e80e2edc45dce9065bda73adc7e9337b64f\n\n\U000000A9Coin Market Cap: coinmarketcap.com/currencies/only-1-token/\n\n\U0001F98ECoin Gecko: coingecko.com/en/coins/only-1-token/\n\n\U0001F4FAYouTube Videos.\nCryptoGains: y2u.be/9PVaduOzPOk\nGoalorious: y2u.be/GdgnpqCwQo8\nCRYPTO RC: youtu.be/2VvXdntQyTY\nVoskCoin: youtu.be/Q7fyUSdZJzU\nConor Kenny: youtu.be/l1Z_vOTj9nA\nFomotion: https://youtu.be/rgezxwD_ctU\n\nMore info at:\n\U0001F30DWebsite: only1token.com/\n\U0001F4ACTelegram: t.me/only1token/\n\U0001F425Twitter: twitter.com/OnlyOneToken/\n\U0001F4F0Medium: only1token.medium.com/\n\U0001F680Reddit: www.reddit.com/r/only1token/\n\U0001F4FAYouTube: youtube.com/c/Only1Token/'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'shillpost\' command: {error}')
        return ERROR_MESSAGES['default']


def get_command_from_body(body):

    message = body.get('message')
    if not message:
        logger.info('[ GET COMMAND ] No message detected in body')
        return None

    message_text = message.get('text')
    if not message_text:
        logger.info('[ GET COMMAND ] No command detected in message')
        return None

    try:
        command = message_text.split('@')[0].split('/')[1]
    except:
        logger.info('[ GET COMMAND ] Failed to parse command')
        return None

    if command in EXCLUDED_COMMANDS:
        logger.info('[ GET COMMAND] Excluded command detected')
        return None

    return command


def lambda_handler(event, context):
    try:
        logger.info(f'[ INIT - EVENT ] {json.dumps(event)}')
        
        body = json.loads(event['body'])
        logger.info(f'[ INIT - BODY ] {json.dumps(body)}')

        command = get_command_from_body(body)
        if not command:
            logger.info(f'[ INIT - COMMAND ] No command')
            return {
                'statusCode': 200
            }

        chat_id = body['message']['chat']['id']

        logger.info('[ INIT ] Validating environment variables')
        for var in ENV_VARS:
            ENV_VARS[var] = os.environ.get(var)
            if ENV_VARS[var] is None:
                raise NameError('Unable to retrieve one or more environment variables')

        api_key =  os.environ['telegramApiKey']
        bot = telebot.TeleBot(api_key, parse_mode='MARKDOWN')
            
        if command == 'holders':
            logger.info('[ COMMAND ] Processing /holders request')
            resp_msg = fetch_holders_command()
            bot.send_photo(chat_id, LINKS['holders_photo'], resp_msg)
        elif command == 'lp_holders':
            logger.info('[ COMMAND ] Processing /lp_holders request')
            resp_msg = fetch_lp_holders()
            bot.send_message(chat_id, resp_msg)
        elif command == 'website':
            logger.info('[ COMMAND ] Processing /website request')
            resp_msg, markup = website()
            bot.send_photo(chat_id, LINKS['website_photo'], resp_msg, reply_markup=markup)
        elif command == 'prices':
            logger.info('[ COMMAND ] Processing /prices request')
            resp_msg = prices()
            bot.send_message(chat_id, resp_msg)
        elif command == 'earningstracker':
            logger.info('[ COMMAND ] Processing /earningstracker request')
            resp_msg, markup = earningstracker()
            bot.send_photo(chat_id, LINKS['earnings_photo'], resp_msg, reply_markup=markup)
        elif command == 'portfoliotracker':
            logger.info('[ COMMAND ] Processing /portfoliotracker request')
            resp_msg, markup = portfoliotracker()
            bot.send_photo(chat_id, LINKS['portfolio_photo'], resp_msg, reply_markup=markup)
        elif command == 'buy':
            logger.info('[ COMMAND ] Processing /buy request')
            resp_msg, markup = buy()
            bot.send_photo(chat_id, LINKS['buy_photo'], resp_msg, reply_markup=markup)
        elif command == 'tax':
            logger.info('[ COMMAND ] Processing /tax request')
            resp_msg = tax()
            bot.send_photo(chat_id, LINKS['tax_photo'], resp_msg)
        elif command == 'slippage':
            logger.info('[ COMMAND ] Processing /slippage request')
            resp_msg = slippage()
            bot.send_message(chat_id, resp_msg)
        elif command == 'chart' or command == f'charts':
            logger.info('[ COMMAND ] Processing /chart request')
            resp_msg, markup = chart()
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
        elif command == 'contract':
            logger.info('[ COMMAND ] Processing /contract request')
            resp_msg = contract()
            bot.send_message(chat_id, resp_msg)
        elif command == 'bscscan':
            logger.info('[ COMMAND ] Processing /bscscan request')
            resp_msg, markup = bscscan()
            bot.send_photo(chat_id, LINKS['bscscan_photo'], resp_msg, reply_markup=markup)
        elif command == 'liquidity':
            logger.info('[ COMMAND ] Processing /liquidity request')
            resp_msg, markup = liquidity()
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
        elif command == 'mediumarticles':
            logger.info('[ COMMAND ] Processing /mediumarticles request')
            resp_msg, markup = mediumarticles()
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
        elif command == 'todolist':
            logger.info('[ COMMAND ] Processing /todolist request')
            resp_msg = todolist()
            bot.send_message(chat_id, resp_msg)
        elif command == 'faq':
            logger.info('[ COMMAND ] Processing /faq request')
            resp_msg, markup = faq()
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
        elif command == 'allcommands':
            logger.info('[ COMMAND ] Processing /allcommands request')
            resp_msg = allcommands()
            bot.send_message(chat_id, resp_msg)
        elif command == 'tokenomics':
            logger.info('[ COMMAND ] Processing /tokenomics request')
            resp_msg, photo = tokenomics()
            bot.send_photo(chat_id, photo, resp_msg)
        elif command == 'mememaker':
            logger.info('[ COMMAND ] Processing /mememaker request')
            resp_msg, markup = mememaker()
            bot.send_photo(chat_id, LINKS['meme_photo'], resp_msg, reply_markup=markup)
        elif command == 'shillpost':
            logger.info('[ COMMAND ] Processing /shillpost request')
            resp_msg = shillpost()
            bot.send_message(chat_id, resp_msg)
        
    except Exception as error:
        logger.error(f'[ FAIL ] Unhandled event: {error}')
        return {
            'statusCode': 200
        }

    return {
        'statusCode': 200
    }