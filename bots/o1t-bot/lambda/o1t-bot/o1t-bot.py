#Only 1 Token

import os
import sys
sys.path.insert(0, '/opt/python/pip_modules')

import simplejson as json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import random

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

import telebot
from telebot import types  # added by adam
from bs4 import BeautifulSoup
import requests
import cloudscraper

import boto3
s3 = boto3.resource('s3')

# Environment Variables
ENV_VARS = {
    'telegramApiKey': '',
    'BOT_NAME': ''
}

NAME = 'Only 1 Token'
SYMBOL = 'O1T'
CONTRACT_ADDRESS = '0xBB994E80E2eDc45dCe9065bda73ADc7E9337b64F'
LP_CONTRACT_ADDRESS = '0x98eeda2abe0a09c6111182c210907d3bf6098efe'

ERROR_MESSAGES = {
    'default': 'Sorry, an error occurred processing your request, wait a few seconds and try again.'
}

LINKS = {
    'website': 'only1token.com',
    'website_photo': 'https://i.ibb.co/TRZHcj9/website.png',
    'lightpaper': 'only1token.medium.com/o1t-lightpaper-8729898a392e',
    'poocoin': f'https://poocoin.app/tokens/{CONTRACT_ADDRESS}',
    'pcs': f'https://pancakeswap.finance/swap?outputCurrency={CONTRACT_ADDRESS}',
    'justswap': f'https://justmoney.exchange/?from=BUSD&n=BSC&t=swap&to=O1T',
    'rewards': f'https://trackbsc.com/earnings?token={CONTRACT_ADDRESS}',
    'portfolio': 'https://trackbsc.com/portfolio',
    'bsc': f'https://bscscan.com/token/{CONTRACT_ADDRESS}',
    'bsc_liq': f'https://bscscan.com/address/{LP_CONTRACT_ADDRESS}',
    'bscscan_photo': 'https://i.ibb.co/9HKV2VL/BSCscanv1.jpg',
    'lp_holders': f'https://bscscan.com/token/{LP_CONTRACT_ADDRESS}',
    'holders_photo': 'https://i.ibb.co/2Krv4D9/photo-2021-09-17-10-10-05.jpg',
    'meme': 'https://eyes.justmoney.io/#o1t',
    'meme_photo': 'https://i.ibb.co/FbzfkNz/meme.jpg',
    'bogged': f'https://charts.bogged.finance/?token={CONTRACT_ADDRESS}',
    'dex': f'https://www.dextools.io/app/pancakeswap/pair-explorer/{CONTRACT_ADDRESS}',
    'guru': f'https://dex.guru/token/{CONTRACT_ADDRESS}-bsc',
    'liquidity': 'https://dxsale.app/app/pages/dxlockview?id=0&add=0x83e4152cc57c6A0BBA8bC1F3C658c524Ee28a5f2&type=lplock&chain=BSC',
    'medium': 'https://only1token.medium.com/',
    'medium_photo': 'https://i.ibb.co/PxbZNP8/Medium-Articlesv2.png',
    'faq': 'https://www.reddit.com/r/only1token/comments/ocifwp/o1t_unofficial_faq_created_by_the_community_for/',
    'faq_photo': 'https://i.ibb.co/sKbDMKR/FAQ.png',
    'buy_photo': 'https://i.ibb.co/Jj1LBDp/JMPCSv3.png',
    'tax_photo': 'https://ibb.co/gD71qxN',
    'earnings_photo': 'https://i.ibb.co/TW0x2gN/Rewards-Tracker.jpg',
    'earnings_article': 'https://only1token.medium.com/trackbsc-com-updates-18b5a2dce22a',
    'portfolio_photo': 'https://i.ibb.co/K59pkBd/Portfolio-Tracker.jpg',
    'portfolio_article': 'https://only1token.medium.com/portfolio-tracker-updates-74878209659d'
}

SUPPORTED_COMMANDS = [
    'allcommands',
    'website',
    'earningstracker',
    'portfoliotracker',
    'buy',
    'tax',
    'slippage',
    'chart',
    'contract',
    'bscscan',
    'holders',
    'liquidity',
    'tokenomics',
    'mediumarticles',
    'shillpost',
    'todolist',
    'mememaker',
    'faq',
    'priceinfo',
    'app',
    'dapp',
    'meme'
]

EXCLUDED_COMMANDS = [
#    'prices'
    'price'
]

O1T_MEMES = [
    'https://ibb.co/7rcgm7x',
    'https://ibb.co/zGmxDBg',
    'https://ibb.co/dJjs6yF',
    'https://ibb.co/6Ht4Lsy',
    'https://ibb.co/CJ9njj0',
    'https://ibb.co/LQTXBCv',
    'https://ibb.co/ZJBRdV2',
    'https://ibb.co/WkpspcP',
    'https://ibb.co/VWPqHPn',
    'https://ibb.co/z7Fcx7q',
    'https://ibb.co/v3QQknD',
    'https://ibb.co/HqgKQqN',
    'https://ibb.co/8dZLRSZ',
    'https://ibb.co/6B5Zv6j',
    'https://ibb.co/vxNCtyG',
    'https://ibb.co/bz1qWtK',
    'https://ibb.co/80kjfHq',
    'https://ibb.co/tKtzR7p',
    'https://ibb.co/K7rNDVR',
    'https://ibb.co/4dQVk1v',
    'https://ibb.co/7KSr8fw',
    'https://ibb.co/SnLBB1j',
    'https://ibb.co/VwNwv5k',
    'https://ibb.co/MMb9YXX',
    'https://ibb.co/gVwL3yn',
    'https://ibb.co/YWC96d9',
    'https://ibb.co/8sL5H6t',
    'https://ibb.co/p4BRnZm',
    'https://ibb.co/SmLBhDJ',   
    'https://ibb.co/PQF7vsL',
    'https://ibb.co/25m2VB8',
    'https://ibb.co/n6bgTyH',
    'https://ibb.co/2sjCMzS',
    'https://ibb.co/RBxq3rd',
    'https://ibb.co/F4rB86W',
    'https://ibb.co/n6PDGRn',
    'https://ibb.co/BznTfFd',
    'https://ibb.co/H4vqL81',
    'https://ibb.co/6DKxcq4',
    'https://ibb.co/hchMtVB',
    'https://ibb.co/WGkrHmS',
    'https://ibb.co/Zfd3S3B',
    'https://ibb.co/MNtX6Qk',
    'https://ibb.co/kJ82KJX',
    'https://ibb.co/BGv8DQd',
    'https://ibb.co/LtPZdK0',
    'https://ibb.co/K5m0RwR',
    'https://ibb.co/Ss0fjHF',
    'https://ibb.co/vc7tdNV',
    'https://ibb.co/FhsSk64',
    'https://ibb.co/d2CxD2s',
    'https://ibb.co/grt3KpT',
    'https://ibb.co/yf1ghB7',
    'https://ibb.co/JKTSNT6',
    'https://ibb.co/DzJ8TPr',
    'https://ibb.co/SsCk0zM',
    'https://ibb.co/FD4JykB',
    'https://ibb.co/SKWBYcD',
    'https://ibb.co/kq4T8Fz',
    'https://ibb.co/jghSSRH',
    'https://ibb.co/gwfMw9C',
    'https://ibb.co/gFQK3QB',
    'https://ibb.co/gSxG8yX',
    'https://ibb.co/RQNSqy4',
    'https://ibb.co/vQN1FQK',
    'https://ibb.co/Zdpbd33',
    'https://ibb.co/0DqphZ9',
    'https://ibb.co/2gwkWWm',
    'https://ibb.co/qCbtDMy',
    'https://ibb.co/swKftMy',
    'https://ibb.co/rFvPy5P',
    'https://ibb.co/Ptp4vzb'
]


def allcommands():
    try:
        resp_msg = f'''\U00002139 Here are all commands!\n\n/website - Visit our Website\n/earningstracker - Track your Earned Rewards\n/portfoliotracker - Track your BSC portfolio\n/buy - Buy on PancakeSwap\n/tax - Breakdown of our Tax\n/slippage - Set Slippage on PancakeSwap\n/chart - Check our Charts\n/contract - Contract Address\n/bscscan - BscScan Page\n/holders - Holders of this Token\n/liquidity - Check Locked Liquidity\n/tokenomics - Spiderman Meme\n/mediumarticles - Current List of Medium Articles\n/shillpost - Shill Post for Sharing\n/mememaker - Create a O1T Meme\n/faq - Frequently Asked Questions\n/meme - Post A Random Meme\n/priceinfo - Current Price Info'''
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'allcommands\' command: {error}')
        return ERROR_MESSAGES['default']

def website():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F30D Website',
                                           callback_data='website',
                                           url=LINKS['website'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Click to visit Website!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'website\' command: {error}')
        return ERROR_MESSAGES['default'], None
    

def earningstracker():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U00002705 Earnings Tracker',
                                           callback_data='earningstracker',
                                           url=LINKS['rewards'])
        markup.add(btn_a)
        resp_msg = f'''\n\U00002139 Read more about our Earnings Tracker!\n[Medium Article]({LINKS['earnings_article']})'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'earningstracker\' command: {error}')
        return ERROR_MESSAGES['default'], None


def portfoliotracker():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U00002705 Portfolio Tracker',
                                           callback_data='portfoliotracker',
                                           url=LINKS['portfolio'])
        markup.add(btn_a)
        resp_msg = f'''\n\U00002139 Read more about our Portfolio Tracker!\n[Medium Article]({LINKS['portfolio_article']})'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'portfolio_tracker\' command: {error}')
        return ERROR_MESSAGES['default'], None


def buy():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F95E PancakeSwap(V2)', callback_data='buy', url=LINKS['pcs'])
        btn_b = types.InlineKeyboardButton('\U0001F4B5 JustMoney.Exchange', callback_data='buy', url=LINKS['justswap'])
        markup.add(btn_a)
        markup.add(btn_b)
        resp_msg = f'\U00002139 Buy {NAME} on PancakeSwap(V2) or JustMoney.Exchange, use at least 8% slippage.'
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'buy\' command: {error}')
        return ERROR_MESSAGES['default'], None


def tax():
    try:
        resp_msg = f'\U00002139 {NAME} has a 7% tax on every transfer.\n4.9% goes to holders\n1.9% goes to trading liquidity.\n0.2% goes to our Project Evolution fund'
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'tax\' command: {error}')
        return ERROR_MESSAGES['default']


def slippage():
    try:
        resp_msg = f'''\n\n\U00002139 Set slippage to minimum 8% on PancakeSwap(V2).'''
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'slippage\' command: {error}')
        return ERROR_MESSAGES['default']


def chart():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_bogged = types.InlineKeyboardButton('\U0001F4CA Bogged', callback_data='bogged', url=LINKS['bogged'])
        btn_guru = types.InlineKeyboardButton('\U0001F308 DexGuru', callback_data='guru', url=LINKS['guru'])
        btn_poocoin = types.InlineKeyboardButton('\U0001F4A9 Poocoin', callback_data='poocoin', url=LINKS['poocoin'])
        btn_dex = types.InlineKeyboardButton('\U0001F4A0 DexTools', callback_data='dex', url=LINKS['dex'])
        markup.add(btn_bogged, btn_guru)
        markup.add(btn_poocoin, btn_dex)

        resp_msg = f'''\U00002139 Click any button to use your favorite chart!'''

        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'chart\' command: {error}')
        return ERROR_MESSAGES['default'], None


def contract():
    try:
        resp_msg = f'''\U00002139 Contract Address:\n{CONTRACT_ADDRESS}'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'contract\' command: {error}')
        return ERROR_MESSAGES['default']


def bscscan():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F5A8 BSCscan',
                                           callback_data='bscscan',
                                           url=LINKS['bsc'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Click to view BSCscan!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'bscscan\' command: {error}')
        return ERROR_MESSAGES['default'], None


def liquidity():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F512 Liquidity on DxSale',
                                           callback_data='liquidity',
                                           url=LINKS['liquidity'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139Click the button below. \U0001F512 Liquidity on DxSale!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'liquidity\' command: {error}')
        return ERROR_MESSAGES['default'], None


def tokenomics():
    try:
        photo_url = 'https://t.me/only1token/100088'
        resp_msg = 'Awesome Tokenomics!'
        return resp_msg, photo_url
    except Exception as error:
        logger.error(
            f'Error occurred processing \'tokenomics\' command: {error}')
        return ERROR_MESSAGES['default'], None


def mediumarticles():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F4F0 Medium Articles.',
                                           callback_data='medium_articles',
                                           url=LINKS['medium'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Read our latest Medium Articles!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'medium_articles\' command: {error}')
        return ERROR_MESSAGES['default'], None


def shillpost():
    try:
        resp_msg = f'''[Only 1 Token](only1token.com) is a brand new concept that has never been done before. A single token with 18 decimals, shared by each of its holders who are working together to make O1T the single most valuable asset in the world.\n\n\U0001F947*Our Goal:* Only 1 Token aims to become the most valuable fungible token, while creating tools to help make the Binance Smart Chain ecosystem more user-friendly.\n\n\U0000261DWhile most other crypto projects have trillions of tokens in circulation, we have *Only 1 Token*.\n\nPrice = Market Cap.\n\n\U0001F4B0*Tokenomics*\n7% total tax\n4.9% to holders\n1.9% liquidity pool\n0.2% project evolution fund.\n\n\U0001F48E*Hold to earn*: 4.9% of every transfer of O1T is distributed instantly to each O1T holder’s wallet. This is known as a “reflection fee”, and is achieved through a mechanism originally developed by Reflect Finance, which has been popularized by other projects such as SafeMoon.\n\n\U0001F69C*Hold to farm liquidity*: 5% of every buy and sell is rewarded to LP token holders from the contract reserves as long as funds are available. 25% of the supply was sent to the contract on release of O1T to provide these rewards and it is sustained by the liquidity fee on every transfer. Since 5% of every buy and sell is being rewarded to LP holders and the liquidity fee is only 1.9%, this results in a 3.1% deficit which allows the initial 25% of the supply that is in the contract to slowly decrease  as it enters circulation. Once the contract has paid enough rewards to empty the reserves, the liquidity fee can be reduced to 0%.\n\n\U0001F525*Utility*\n1. TrackBSC.com is free. Check what you’ve earned from reflect rewards on ANY #BSC token that offers RFI. You are also shown the liquidity adjusted price, giving you more accurate pricing.\n\U0001F449[Earnings Article](only1token.medium.com/trackbsc-com-updates-18b5a2dce22a)\n\n2. *Portfolio Tracker*: Track your holdings, their current market price, their liquidity adjusted value and easily trade them on PancakeSwap with a press of a button! When viewing your portfolio, you can select any of your tokens and it will direct you to the info/rewards page for that token. This will facilitate a more user-friendly navigation through your portfolio and their respective reflection rewards rather than searching for each token manually. Furthermore, additional features such as viewing other wallet’s portfolio can be unlocked by either holding $60 worth of BNB-O1T in liquidity. This feature would allow users to easily check what other wallets (such as whales) are investing in and the liquidity adjusted value of each of their holdings.\n\U0001F449[Portfolio Article](only1token.medium.com/portfolio-tracker-updates-74878209659d)\n\n\U0001F4D1Contract Address:\n0xbb994e80e2edc45dce9065bda73adc7e9337b64f\n\n\U0001F5A8[BSCscan](bscscan.com/token/0xbb994e80e2edc45dce9065bda73adc7e9337b64f)\n\n\U000000A9[Coin Market Cap](coinmarketcap.com/currencies/only-1-token/)\n\U0001F98E[Coin Gecko](coingecko.com/en/coins/only-1-token/)\n\n\U0001F4FAYouTube Videos.\n[CryptoGains](y2u.be/9PVaduOzPOk)\n[Goalorious](y2u.be/GdgnpqCwQo8)\n[CRYPTO RC](youtu.be/2VvXdntQyTY)\n[VoskCoin](youtu.be/Q7fyUSdZJzU)\n[Conor Kenny](youtu.be/l1Z_vOTj9nA)\n[Fomotion](https://youtu.be/rgezxwD_ctU)\n\nMore info at:\n\U0001F30D[Website](only1token.com/)\n\U0001F4AC[Telegram](t.me/only1token/)\n\U0001F425[Twitter](twitter.com/OnlyOneToken/)\n\U0001F4F0[Medium](only1token.medium.com/)\n\U0001F680[Reddit](www.reddit.com/r/only1token/)\n\U0001F4FA[YouTube](youtube.com/c/Only1Token/)'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'shillpost\' command: {error}')
        return ERROR_MESSAGES['default']


def mememaker():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F525 Create your own O1T Meme \U0001F525',
                                           callback_data='mememaker',
                                           url=LINKS['meme'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Make your own Only 1 Token Meme!\n\n\U00002705 Show JustMoney.io some love for making the O1T meme generator.'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'mememaker\' command: {error}')
        return ERROR_MESSAGES['default'], None


def faq():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('Frequently Asked Questions \U0001F4AC',
                                           callback_data='faq',
                                           url=LINKS['faq'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 We have summarized all questions in our FAQ on Reddit.'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'faq\' command: {error}')
        return ERROR_MESSAGES['default'], None


def meme():
    try:
        resp_msg = ''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'meme\' command: {error}')
        return ERROR_MESSAGES['default']


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
                liq_tokens['WBNB'] = span.text.split('.')[0]
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


def priceinfo():
    try: 
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F95E PancakeSwap(V2)', callback_data='buy', url=LINKS['pcs'])
        btn_b = types.InlineKeyboardButton('\U0001F4B5 JustMoney.Exchange', callback_data='buy', url=LINKS['justswap'])
        markup.add(btn_a)
        markup.add(btn_b)

        return markup
    except Exception as error:
        logger.error(f'Error occurred processing \'prices\' command: {error}')
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
            print(var)
            ENV_VARS[var] = os.environ.get(var)
            if ENV_VARS[var] == '':
                raise NameError('Unable to retrieve one or more environment variables')

        api_key = ENV_VARS['telegramApiKey']
        print(ENV_VARS)
        bot = telebot.TeleBot(api_key, parse_mode='MARKDOWN')
            
        if command == 'allcommands':
            logger.info('[ COMMAND ] Processing /allcommands request')
            resp_msg = allcommands()
            bot.send_message(chat_id, resp_msg)
            
        elif command == 'website':
            logger.info('[ COMMAND ] Processing /website request')
            resp_msg, markup = website()
            bot.send_photo(chat_id, LINKS['website_photo'], resp_msg, reply_markup=markup)
            
        elif command == 'earningstracker':
            logger.info('[ COMMAND ] Processing /earningstracker request')
            resp_msg, markup = earningstracker()
            bot.send_photo(chat_id, LINKS['earnings_photo'], resp_msg, reply_markup=markup)
            
        elif command == 'portfoliotracker' or command == f'app'  or command == f'dapp':
            logger.info('[ COMMAND ] Processing /portfoliotracker request')
            resp_msg, markup = portfoliotracker()
            bot.send_photo(chat_id, LINKS['portfolio_photo'], resp_msg, reply_markup=markup)
            
        elif command == 'buy' or command == f'pcs':
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
            
        elif command == 'holders':
            logger.info('[ COMMAND ] Processing /holders request')
            resp_msg = fetch_holders_command()
            bot.send_photo(chat_id, LINKS['holders_photo'], resp_msg)
            
        elif command == 'liquidity':
            logger.info('[ COMMAND ] Processing /liquidity request')
            resp_msg, markup = liquidity()
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
        elif command == 'tokenomics':
            logger.info('[ COMMAND ] Processing /tokenomics request')
            resp_msg, photo = tokenomics()
            bot.send_photo(chat_id, photo, resp_msg)
            
        elif command == 'mediumarticles':
            logger.info('[ COMMAND ] Processing /mediumarticles request')
            resp_msg, markup = mediumarticles()
            bot.send_photo(chat_id, LINKS['medium_photo'], resp_msg, reply_markup=markup)
            
        elif command == 'shillpost':
            logger.info('[ COMMAND ] Processing /shillpost request')
            resp_msg = shillpost()
            bot.send_message(chat_id, resp_msg)
            
        elif command == 'mememaker':
            logger.info('[ COMMAND ] Processing /mememaker request')
            resp_msg, markup = mememaker()
            bot.send_photo(chat_id, LINKS['meme_photo'], resp_msg, reply_markup=markup)
            
        elif command == 'faq':
            logger.info('[ COMMAND ] Processing /faq request')
            resp_msg, markup = faq()
            bot.send_photo(chat_id, LINKS['faq_photo'], resp_msg, reply_markup=markup)
            
        elif command == 'meme':
            logger.info('[ COMMAND ] Processing /meme request')
            resp_msg = meme()
            bot.send_photo(chat_id, random.choice(O1T_MEMES), resp_msg)
            
        elif command == 'priceinfo':
            logger.info('[ COMMAND ] Processing /priceinfo request')
            logger.info('Getting files from s3')
            s3.meta.client.download_file('price-processor', 'only-1-token.png', '/tmp/only-1-token.png')
            s3.meta.client.download_file('price-processor', 'only-1-token.txt', '/tmp/only-1-token.txt')
            logger.info('Files downloaded')
            resp_msg = ''
            with open('/tmp/only-1-token.txt') as f:
                resp_msg = f.read()
            markup = priceinfo()
            bot.send_photo(chat_id, open('/tmp/only-1-token.png', 'rb'), resp_msg, reply_markup=markup)
        
    except Exception as error:
        logger.error(f'[ FAIL ] Unhandled event: {error}')
        return {
            'statusCode': 200
        }

    return {
        'statusCode': 200
    }