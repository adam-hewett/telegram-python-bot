#Infinite One MAIN bot


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

NAME = 'Project Quantum'
SYMBOL = 'QBIT'
CONTRACT_ADDRESS = '0xa38898a4ae982cb0131104a6746f77fa0da57aaa'
LP_CONTRACT_ADDRESS = '0xE39C55fb2aB7d9b6888bcc5178A44eBB0CF42BbB'
SUPPLY = '1'

ERROR_MESSAGES = {
    'default': 'Sorry, an error occurred processing your request, wait a few seconds and try again.'
}

LINKS = {

    'website': 'https://quantumworks.co.uk',
    'whitepaper': 'https://cdn.flowcode.com/prodassets/Project_Quantum_Rev1.1.pdf?ts=1626173498462526627',
    'pcs': f'https://pancakeswap.finance/swap?outputCurrency={CONTRACT_ADDRESS}',
    'rewards': f'https://trackbsc.com/earnings?token={CONTRACT_ADDRESS}',
#    'dapp': 'https://trackbsc.com/portfolio',
    'bsc': f'https://bscscan.com/token/{CONTRACT_ADDRESS}',
    'bsc_liq': f'https://bscscan.com/address/{LP_CONTRACT_ADDRESS}',
    'lp_holders': f'https://bscscan.com/token/{LP_CONTRACT_ADDRESS}',
    'lock_liq': 'https://app.unicrypt.network/amm/pancake-v2/token/0xA38898a4Ae982Cb0131104a6746f77fA0dA57aAA',
#    'faq': 'https://www.reddit.com/r/only1token/comments/ocifwp/o1t_unofficial_faq_created_by_the_community_for/',
    
    'poocoin': f'https://poocoin.app/tokens/{CONTRACT_ADDRESS}',
    'bogged': f'https://charts.bogged.finance/?token={CONTRACT_ADDRESS}',
    'dex': f'https://www.dextools.io/app/pancakeswap/pair-explorer/{CONTRACT_ADDRESS}',
    'guru': f'https://dex.guru/token/{CONTRACT_ADDRESS}-bsc',
    
    'website_photo': 'https://i.ibb.co/QDjW41N/website.jpg',
    'buy_photo': 'https://i.ibb.co/C77NwNS/PCSv2.jpg',
    'bscscan_photo': 'https://i.ibb.co/9HKV2VL/BSCscanv1.jpg',
    'tax_photo': 'https://ibb.co/gD71qxN',
    'holders_photo': 'https://i.ibb.co/2Krv4D9/photo-2021-09-17-10-10-05.jpg',
    'rewards_photo': 'https://i.ibb.co/TW0x2gN/Rewards-Tracker.jpg',
    'dapp_photo': 'https://i.ibb.co/K59pkBd/Portfolio-Tracker.jpg',
    'medium_photo': 'https://i.ibb.co/PxbZNP8/Medium-Articlesv2.png',
    
    'medium': 'https://only1token.medium.com/',
    'portfolio_article': 'https://only1token.medium.com/portfolio-tracker-updates-74878209659d',
    'rewards_article': 'https://only1token.medium.com/trackbsc-com-updates-18b5a2dce22a',
    
    'Reddit': 'https://www.reddit.com/r/ProjectQuantum_',
    'Instagram': 'https://www.instagram.com/projectquantum_/',
    'Twitter': 'https://twitter.com/projectquantum_',
    'Discord': 'https://discord.gg/x8GK6heCgs',
    'Twitch': 'https://www.twitch.tv/project_quantum',
    'Facebook': 'https://www.facebook.com/projectquantumofficial',
    'Discord': 'https://discord.gg/ProjectQuantum',
    'Youtube': 'https://www.youtube.com/channel/UCzztOczpxcXuXoAWRM0qAHA'

}

SUPPORTED_COMMANDS = [
    'allcommands',
    'website',
    'web',
    'whitepaper',
    'lightpaper',
    'rewards',
    'buy',
    'pcs',
    'tokenomics',
    'tax',
    'slippage',
    'chart',
    'charts',
    'contract',
    'bscscan',
    'holders',
    'liquidity',
    'faq',
    'priceinfo',
    'airdrop',
    'channels',
    'groups',
    'international',
    'nft',
    'ban',
    'socials',
    'marketing'
]

EXCLUDED_COMMANDS = [
#    'prices'
    'price'
]

def allcommands():
    try:
        resp_msg = f'''\U00002139 Here are all commands!\n\n/website - Visit Website\n/rewards - Track your Rewards \n/airdrop - Air Drop Explained\n/channels - All Channels and Groups\n/nft - NFT Collections\n/tax - Tax Explained\n/tokenomics - Tokenomics Explained\n/ban - Group Policy\n/whitepaper - Our White Paper\n/contract - Contract Address & BscScan Page\n/buy - Buy on PancakeSwap(V2)\n/chart - Price Chartsn\n/holders - FatCake Holders\n/liquidity - Locked Liquidity\n/socials - Social Media\n/marketing - Direct Marketing Proposals\n/price\_info - Get Price Info'''
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
    

def whitepaper():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F4D1 Whitepaper.',
                                           callback_data='whitepaper',
                                           url=LINKS['whitepaper'])
        markup.add(btn_a)
        resp_msg = f'''\n\U00002139 Read our Whitepaper.'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'whitepaper\' command: {error}')
        return ERROR_MESSAGES['default'], None


def rewards():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U00002705 Track Your Rewards.',
                                           callback_data='rewards',
                                           url=LINKS['rewards'])
        markup.add(btn_a)
        resp_msg = f'''\n\U00002139 Check your QBIT reflection rewards on TrackBSC.com!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'rewards\' command: {error}')
        return ERROR_MESSAGES['default'], None


def buy():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F95E PancakeSwap(V2)',
                                           callback_data='buy',
                                           url=LINKS['pcs'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Sounds like you're ready to buy! Excellent choice friend, I hope you understand the tokenomics. Welcome to the future of gaming! Use 12% slippage.'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'buy\' command: {error}')
        return ERROR_MESSAGES['default'], None


def tokenomics():
    try:
        resp_msg = f'\U00002139 {NAME} has a 10% Taxes on any transaction.\n├3.0% is reflected to our holders.\n├3.5% is converted to BNB and sent to fund the game studio. \n└3.5% will be held to reward our players once the game launches.'
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'tokenomics\' command: {error}')
        return ERROR_MESSAGES['default']


def slippage():
    try:
        resp_msg = f'''\n\n\U00002139 Set slippage to minimum 12% on PancakeSwap(V2).'''
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'slippage\' command: {error}')
        return ERROR_MESSAGES['default']


def charts():
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
        logger.error(f'Error occurred processing \'charts\' command: {error}')
        return ERROR_MESSAGES['default'], None


def socials():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F4CA Twitter', callback_data='twitter', url=LINKS['twitter'])
        btn_b = types.InlineKeyboardButton('\U0001F308 Facebook', callback_data='facebook', url=LINKS['facebook'])
        btn_c = types.InlineKeyboardButton('\U0001F4A9 Instagram', callback_data='instagram', url=LINKS['instagram'])
        btn_d = types.InlineKeyboardButton('\U0001F4A0 Reddit', callback_data='reddit', url=LINKS['reddit'])
        btn_e = types.InlineKeyboardButton('\U0001F4A0 YouTube', callback_data='youtube', url=LINKS['youtube'])
        btn_f = types.InlineKeyboardButton('\U0001F4A0 Discord', callback_data='discord', url=LINKS['discord'])
        btn_g = types.InlineKeyboardButton('\U0001F4A0 Twitch', callback_data='twitch', url=LINKS['twitch'])
        markup.add(btn_a, btn_b, btn_c)
        markup.add(btn_d, btn_e, btn_f, btn_g)

        resp_msg = f'''\U00002139 Follow our Social Media Channels!'''

        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'socials\' command: {error}')
        return ERROR_MESSAGES['default'], None


def contract():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F5A8 BSCscan Contract Page', callback_data='bscscan', url=LINKS['bsc'])
        btn_b = types.InlineKeyboardButton('\U0001F5A8 BSCscan LP Contract Page', callback_data='bsc_liq', url=LINKS['bsc_liq'])

        markup.add(btn_a)
        markup.add(btn_b)
        resp_msg = f'''{CONTRACT_ADDRESS}'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'bscscan\' command: {error}')
        return ERROR_MESSAGES['default'], None


def liquidity():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F512 Liquidity on Unicrypt.network',
                                           callback_data='liquidity',
                                           url=LINKS['lock_liq'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139Click the button below. \U0001F512 Liquidity on Unicrypt.network!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'liquidity\' command: {error}')
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


def airdrop():
    try:
        resp_msg = f'1. Airdrops are not an obligation. They are a reward, decided upon by the core team, for those who held through the tougher periods of Quantum. Even smaller holders have received some. It hasn’t been limited to solely early adopters, as those who can meet the requirements are welcome to participate.\n\n2. Reflections are part of the contract and are a given to ALL community. This is something that rewards EVERYONE.\n\n3. We’ve heard your suggestion, so please respect the fact that we’ve borne in mind what you’ve said. I’ve seen a few times now that admins have acknowledged what you’ve said, so I’d like us to end beating a dead horse. \n\nThe core team will determine it as they see fit as they are the ones who put it into action.'
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'slippage\' command: {error}')
        return ERROR_MESSAGES['default']


def airdrop():
    try:
        resp_msg = f'1. Airdrops are not an obligation. They are a reward, decided upon by the core team, for those who held through the tougher periods of Quantum. Even smaller holders have received some. It hasn’t been limited to solely early adopters, as those who can meet the requirements are welcome to participate.\n\n2. Reflections are part of the contract and are a given to ALL community. This is something that rewards EVERYONE.\n\n3. We’ve heard your suggestion, so please respect the fact that we’ve borne in mind what you’ve said. I’ve seen a few times now that admins have acknowledged what you’ve said, so I’d like us to end beating a dead horse. \n\nThe core team will determine it as they see fit as they are the ones who put it into action.'
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'slippage\' command: {error}')
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
        resp_msg = f'''\U0001F4B0 {SYMBOL} Holders: *{holders.strip()}*\n\U00002139 All {SYMBOL} holders earn 4.9% of every token transfer.\n\n\U0001F4B0 BNB/{SYMBOL} LP Holders: *{lp_holders.strip()}*\n\U00002139 All BNB/{SYMBOL} LP holders earn 5% of every Buy and Sell.'''
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


def priceinfo():
    try: 
        price_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=only-1-token%2Cbinancecoin&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true')
        price_data = price_response.json()
        o1t_price = "${:,.0f}".format(price_data['only-1-token']['usd'])
        o1t_change = int(price_data['only-1-token']['usd_24h_change'])
        o1t_vol = "${:,.0f}".format(price_data['only-1-token']['usd_24h_vol'])
        
        get_marketcap = float((price_data['only-1-token']['usd']) * 1)
        marketcap = locale.currency( get_marketcap, grouping=True ).split('.')[0]
        
        bnb_price = locale.currency( price_data['binancecoin']['usd'], grouping=True )
        bnb_change = int(price_data['binancecoin']['usd_24h_change'])
        
        holders = fetch_holders()
        lp_holders=fetch_lp_holders()
        
        liq_tokens = get_liquidity_tokens()
        bnb_liq_value = float(liq_tokens['WBNB']) * float(price_data['binancecoin']['usd'])
        bnb_liq_dlr_value = locale.currency( bnb_liq_value, grouping=True )
        o1t_liq_value = float(liq_tokens['O1T']) * float(price_data['only-1-token']['usd'])
        o1t_liq_dlr_value = locale.currency( o1t_liq_value, grouping=True )
        liq_total = locale.currency( float(bnb_liq_value) + float(o1t_liq_value), grouping=True )
        
        bnb_o1t_value = (float(price_data['only-1-token']['usd']) / float(price_data['binancecoin']['usd']) * 0.010753)
        bnb_o1t_dlr_value = locale.currency( bnb_o1t_value, grouping=True ).split('$')[1]
        
        o1t_bnb_value = (1 / (float(price_data['only-1-token']['usd']) / float(price_data['binancecoin']['usd'])))
        o1t_bnb_dlr_value = "${:,.8f}".format( o1t_bnb_value, grouping=True ).split('$')[1]
        
        resp_msg = f'''Current price information\n\nName: *{NAME}*\nSymbol: *{SYMBOL}*\n\n{SYMBOL} Price: *{o1t_price} ({o1t_change}%) 24H*\nMarket Cap: *{marketcap}*\n24H Volume: *{o1t_vol}*\nHolders: *{holders.strip()}*\n\nLiquidity Total: *{liq_total}*\nLiquidity {SYMBOL} Qty: *{liq_tokens['O1T']}*\nLiquidity {SYMBOL} Value: *{o1t_liq_dlr_value}*\nLiquidity BNB Qty: *{liq_tokens['WBNB']}*\nLiquidity BNB Value: *{bnb_liq_dlr_value}*\nLP Holders: *{lp_holders.strip()}*\n\nBNB Price: *{bnb_price} ({bnb_change}%) 24H*\n\n1 BNB = *{o1t_bnb_dlr_value} {SYMBOL}*\n{bnb_o1t_dlr_value} BNB = 1% O1T Supply'''
        return resp_msg
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
            ENV_VARS[var] = os.environ.get(var)
            if ENV_VARS[var] is None:
                raise NameError('Unable to retrieve one or more environment variables')

        api_key =  os.environ['telegramApiKey']
        bot = telebot.TeleBot(api_key, parse_mode='MARKDOWN')
            
        if command == 'allcommands':
            logger.info('[ COMMAND ] Processing /allcommands request')
            resp_msg = allcommands()
            bot.send_message(chat_id, resp_msg)
            
        elif command == 'website':
            logger.info('[ COMMAND ] Processing /website request')
            resp_msg, markup = website()
#            bot.send_photo(chat_id, LINKS['website_photo'], resp_msg, reply_markup=markup)
            bot.send_message(chat_id, resp_msg, reply_markup=markup)

        elif command == 'lightpaper' or command == f'litepaper':
            logger.info('[ COMMAND ] Processing /lightpaper request')
            resp_msg, markup = lightpaper()
#            bot.send_photo(chat_id, LINKS['lightpaper_photo'], resp_msg, reply_markup=markup)
            bot.send_message(chat_id, resp_msg, reply_markup=markup)

        elif command == 'rewards':
            logger.info('[ COMMAND ] Processing /rewards request')
            resp_msg, markup = rewards()
#            bot.send_photo(chat_id, LINKS['rewards_photo'], resp_msg, reply_markup=markup)
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
        elif command == 'dapp' or command == f'app':
            logger.info('[ COMMAND ] Processing /dapp request')
            resp_msg, markup = dapp()
#            bot.send_photo(chat_id, LINKS['dapp_photo'], resp_msg, reply_markup=markup)
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
        elif command == 'buy' or command == f'pcs':
            logger.info('[ COMMAND ] Processing /buy request')
            resp_msg, markup = buy()
#            bot.send_photo(chat_id, LINKS['buy_photo'], resp_msg, reply_markup=markup)
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
        elif command == 'tokenomics' or command == f'tax':
            logger.info('[ COMMAND ] Processing /tokenomics request')
            resp_msg = tokenomics()
#            bot.send_photo(chat_id, LINKS['tax_photo'], resp_msg)
            bot.send_message(chat_id, resp_msg)
            
        elif command == 'slippage':
            logger.info('[ COMMAND ] Processing /slippage request')
            resp_msg = slippage()
#            bot.send_photo(chat_id, LINKS['slippage_photo'], resp_msg)
            bot.send_message(chat_id, resp_msg)
            
        elif command == 'chart' or command == f'charts':
            logger.info('[ COMMAND ] Processing /charts request')
            resp_msg, markup = charts()
#            bot.send_photo(chat_id, LINKS['charts_photo'], resp_msg, reply_markup=markup)
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
            elif command == 'channels' or command == f'groups':
            logger.info('[ COMMAND ] Processing /channels request')
            resp_msg, markup = channels()
#            bot.send_photo(chat_id, LINKS['charts_photo'], resp_msg, reply_markup=markup)
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
        elif command == 'contract' or command == f'bscscan' or command == f'bsc':
            logger.info('[ COMMAND ] Processing /contract request')
            resp_msg, markup = contract()
#            bot.send_photo(chat_id, LINKS['bscscan_photo'], resp_msg, reply_markup=markup)
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
        elif command == 'mediumarticles':
            logger.info('[ COMMAND ] Processing /mediumarticles request')
            resp_msg, markup = mediumarticles()
#            bot.send_photo(chat_id, LINKS['medium_photo'], resp_msg, reply_markup=markup)
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
        elif command == 'holders':
            logger.info('[ COMMAND ] Processing /holders request')
            resp_msg = fetch_holders_command()
#            bot.send_photo(chat_id, LINKS['holders_photo'], resp_msg)
            bot.send_message(chat_id, resp_msg)
            
        elif command == 'liquidity':
            logger.info('[ COMMAND ] Processing /liquidity request')
            resp_msg, markup = liquidity()
#            bot.send_photo(chat_id, LINKS['liq_photo'], resp_msg, reply_markup=markup)
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
        elif command == 'faq':
            logger.info('[ COMMAND ] Processing /faq request')
            resp_msg, markup = faq()
#            bot.send_photo(chat_id, LINKS['faq_photo'], resp_msg, reply_markup=markup)
            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
        elif command == 'priceinfo':
            logger.info('[ COMMAND ] Processing /priceinfo request')
            resp_msg = priceinfo()
            bot.send_message(chat_id, resp_msg)
        
    except Exception as error:
        logger.error(f'[ FAIL ] Unhandled event: {error}')
        return {
            'statusCode': 200
        }

    return {
        'statusCode': 200
    }