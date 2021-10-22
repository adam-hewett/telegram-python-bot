#MAIN FatCake Bot

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

# Environment Variables
ENV_VARS = {
    'telegramApiKey': '',
    'BOT_NAME': ''
}

CONTRACT_ADDRESS = '0xB7Dba4C673beDB174DC3Ff7Ec65d17C863d39b16'

ERROR_MESSAGES = {
    'default': 'Sorry, an error occurred processing your request, wait a few seconds and try again.'
}

LINKS = {
    'website': 'https://www.fatecosystem.com/ecosystem',
    'website_photo': 'https://i.ibb.co/tCkPNsG/Place-Holder.png',
    'fatpay': 'https://fatpay.to/',
    'fatpad': 'https://www.fatecosystem.com/fatpad',
    'rewards': 'https://fatcakerewards.netlify.app',
    'rewards_photo': 'https://i.ibb.co/tCkPNsG/Place-Holder.png',
    'pcs': 'https://pancakeswap.finance/swap?outputCurrency=0xB7Dba4C673beDB174DC3Ff7Ec65d17C863d39b16',
    'pcs_photo': 'https://i.ibb.co/tCkPNsG/Place-Holder.png',
    'tax_photo': 'https://i.ibb.co/tCkPNsG/Place-Holder.png',
    'slippage_photo': '',
    'chart_photo': '',
    'bscscan': 'https://bscscan.com/token/0xB7Dba4C673beDB174DC3Ff7Ec65d17C863d39b16',
    'bscscan_photo': 'https://i.ibb.co/tCkPNsG/Place-Holder.png',
    'bsc_liq': 'https://bscscan.com/address/0x6612879d031846723ecf7322afb4f3a97a045dc2',
    'holders_photo': 'https://i.ibb.co/M55HX2k/Neon-Effect.png',
    'liquidity': 'https://dxsale.app/app/v2_9/dxlockview?id=1805&add=0&type=lpdefi&chain=BSC',
    'whitepaper': 'https://ba1eeeb9-8780-4702-a175-a98ed2b9ba07.filesusr.com/ugd/8b9157_38f9aa8f32d14a61891d9fb2d1b05154.pdf',
    'whitepaper_photo': 'https://i.ibb.co/YyJtJmN/Pink-Paper-banner.png',
    'merch': 'https://www.fatecosystem.com/shop',
    'merch_photo': 'https://i.ibb.co/z5mLmpM/Merch.png',
    'nft': 'https://treasureland.market/homepage?address=0xa7c3aabf911b8ff6cdf61eb9eb5147fe5d8bfddd',
    'nft_2': 'https://opensea.io/collection/frosting-social-avatar-collection',
    'rowdy_nft': 'https://opensea.io/collection/rowdyrabbits',
    'nft_photo': 'https://i.ibb.co/tCkPNsG/Place-Holder.png',
    'poocoin': 'https://poocoin.app/tokens/0xB7Dba4C673beDB174DC3Ff7Ec65d17C863d39b16',
    'bogged': 'https://charts.bogged.finance/0xB7Dba4C673beDB174DC3Ff7Ec65d17C863d39b16',
    'dex': 'https://www.dextools.io/app/pancakeswap/pair-explorer/0xB7Dba4C673beDB174DC3Ff7Ec65d17C863d39b16',
    'guru':'https://dex.guru/token/0xB7Dba4C673beDB174DC3Ff7Ec65d17C863d39b16-bsc',
    
    'usa': 'https://t.me/FatEcosystem',
    'china': 'https://t.me/FATEcosystemCH', 
    'germany': 'https://t.me/FATEcosystemDE',
    'india': 'https://t.me/FATEcosystemIN', 
    'italian': 'https://t.me/FATEcosystemIT',
    'japan': 'https://t.me/FATEcosystemJP',
    'arab': 'https://t.me/FATEcosystemAr',
    'spain': 'https://t.me/FATEcosystemSP',
    'promotion': 't.me/fatpromo'
}

FATCAKE_IMAGES = [
    'https://i.ibb.co/zhVj5v8/FCB1.jpg',
    'https://i.ibb.co/BVPNzYt/FCB2.jpg',
    'https://i.ibb.co/wzwxDsb/FCB3.jpg',
    'https://i.ibb.co/PtPLk3j/FCB4.jpg',
    'https://i.ibb.co/cbNMTLq/FCB01.jpg',
    'https://i.ibb.co/DwVWznd/FCB03.jpg',
    'https://i.ibb.co/xJHm5my/FCB02.jpg',
    'https://i.ibb.co/N6ZgyDJ/FCB05.png',
    'https://i.ibb.co/tc6BQt4/FCB06.png',
    'https://i.ibb.co/Fbn32YV/FCB07.png',
    'https://i.ibb.co/tpTtQNh/FCB08.png'
]

FROSTING_IMAGES = [
    'https://i.ibb.co/hXBvrqt/Frosting-2.png',
    'https://i.ibb.co/d6dCJbZ/Frosting-1.png',
    'https://i.ibb.co/mJD77wG/PSfilled.png',
    'https://i.ibb.co/z8s8hQJ/FCB04.png'
]


#allcommands - Show All Commands
#website - Visit Website
#rewards - Track your Rewards
#buy - Buy on PancakeSwap(V2)
#tax - Tax Explained
#slippage - Set Slippage on PancakeSwap(V2)
#chart - Price Charts
#contract - Contract Address
#bscscan - BscScan Page
#holders - FatCake Holders
#liquidity - Locked Liquidity
#tokenomics - Tokenomics Explained
#nft - NFT Collections
#whitepaper - The F.A.T. Ecosystem White Paper
#merch - Buy Fatcake / Frosting Merch
#frosting - Frosting Social
#channels - Fatcake International Telegram Groups
#hashtags - Recommended Hashtags
#marketing - Direct Marketing Proposals
#price_info - Get Price Info
#vote - Voting Websites


SUPPORTED_COMMANDS = [
    'allcommands',
    'website',
    'rewards',
    'buy',
    'tax',
    'slippage',
    'chart',
    'contract',
    'bscscan',
    'holders',
    'liquidity',
    'tokenomics',
    'nft',
    'pinkpaper',
    'whitepaper',
    'merch',
    'store',
    'channels',
    'hashtags',
    'price_info',
    'marketing',
    'frosting',
    'WE_ARE_BUILDING_THIS',
    'REAL_BUSINESS',
    'REAL_VALUE',
    'REAL_UTILITY',
    'FOR_THE_REAL_WORLD',
    'BRICK_BY_BRICK',
    'WE_DETERMINE_OUR_OWN_FATE',
    'WE_WILL_NOT_BE_DETERRED',
    'report',
    'vote'
]

EXCLUDED_COMMANDS = [
#    'prices',
    'price'
]


def allcommands():
    try:
        resp_msg = f'''\U00002139 Here are all commands!\n\n/allcommands - Show All Commands\n/website - Visit Website\n/rewards - Track your Rewards\n/buy - Buy on PancakeSwap(V2)\n/tax - Tax Explained\n/slippage - Set Slippage on PancakeSwap(V2)\n/chart - Price Charts\n/contract - Contract Address\n/bscscan - BscScan Page\n/holders - FatCake Holders\n/liquidity - Locked Liquidity\n/tokenomics - Tokenomics Explained\n/nft - NFT Collections\n/whitepaper - The F.A.T. Ecosystem White Paper\n/merch - Buy Fatcake / Frosting Merch\n/frosting - Frosting Social\n/channels - International Telegram Groups\n/hashtags - Recommended Hashtags\n/marketing - Direct Marketing Proposals\n/price\_info - Get Price Info\n/vote - Voting Websites'''
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'allcommands\' command: {error}')
        return ERROR_MESSAGES['default']


def website(): #done FC
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('🌍 Fat Ecosystem', callback_data='website', url=LINKS['website'])
        btn_b = types.InlineKeyboardButton('💸 Fat Pay', callback_data='fatpay', url=LINKS['fatpay'])
        btn_c = types.InlineKeyboardButton('🚀 Fat Pad', callback_data='fatpad', url=LINKS['fatpad'])
        markup.add(btn_a)
        markup.add(btn_b)
        markup.add(btn_c)
        resp_msg = f'''\U00002139 Click the button to visit our Websites!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'website\' command: {error}')
        return ERROR_MESSAGES['default'], None


def rewards(): #done FC
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('Check \U0001F9C1 Rewards',
                                           callback_data='rewards',
                                           url=LINKS['rewards'])
        markup.add(btn_a)
        resp_msg = f'''\n\U00002139 Click the button to check your rewards!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'rewards\' command: {error}')
        return ERROR_MESSAGES['default'], None


def buy(): #done FC
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F95E PancakeSwap(V2)', callback_data='buy', url=LINKS['pcs'])
        markup.add(btn_a)
        resp_msg = '\U00002139 Buy FatCake on PancakeSwap(V2), use at least 15% slippage.'
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'buy\' command: {error}')
        return ERROR_MESSAGES['default'], None


def tax(): #done FC
    try:
        resp_msg = f'''\U00002139 Every Transaction is charged a *15% tax*, which is split into three separate functions.\n\n*10%* is converted into CAKE and distributed to holders.\n*3%* is converted to CAKE and sent to a marketing wallet.\n*2%* is directly injected into the Liquidity Pool'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'tax\' command: {error}')
        return ERROR_MESSAGES['default']


def slippage(): #done FC
    try:
        resp_msg = f'''\n\n\U00002139 Set slippage to minimum 15% on PancakeSwap(V2).'''
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'slippage\' command: {error}')
        return ERROR_MESSAGES['default']


def chart(): #done FC
    try:
        markup = types.InlineKeyboardMarkup()
        btn_bogged = types.InlineKeyboardButton('\U0001F4CABogged', callback_data='bogged', url=LINKS['bogged'])
        btn_guru = types.InlineKeyboardButton('\U0001F308DexGuru', callback_data='guru', url=LINKS['guru'])
        btn_poocoin = types.InlineKeyboardButton('\U0001F4A9Poocoin', callback_data='poocoin', url=LINKS['poocoin'])
        btn_dex = types.InlineKeyboardButton('\U0001F4A0DexTools', callback_data='dex', url=LINKS['dex'])
        markup.add(btn_bogged, btn_guru)
        markup.add(btn_poocoin, btn_dex)
        
        resp_msg = f'''\U00002139 Click any button below and use your favorite chart!'''
        
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'chart\' command: {error}')
        return ERROR_MESSAGES['default'], None


def contract(): #done FC
    try:
        resp_msg = f'''\U00002139 FatCake Contract Address:\n0xB7Dba4C673beDB174DC3Ff7Ec65d17C863d39b16'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'contract\' command: {error}')
        return ERROR_MESSAGES['default']


def bscscan(): #done FC
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F5A8BSCscan',
                                           callback_data='bscscan',
                                           url=LINKS['bscscan'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Click the button below to view BSCscan!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'bscscan\' command: {error}')
        return ERROR_MESSAGES['default'], None


def liquidity(): #done FC
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F512Liquidity on DxSale',
                                           callback_data='liquidity',
                                           url=LINKS['liquidity'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Click the button below. \n\U0001F512 Liquidity on DxSale!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'liquidity\' command: {error}')
        return ERROR_MESSAGES['default'], None


def tokenomics(): #done FC
    try:
        photo_url = 'https://i.ibb.co/HCVNFbT/photo-2021-09-23-19-05-25.jpg'
        resp_msg = ''
        return resp_msg, photo_url
    except Exception as error:
        logger.error(
            f'Error occurred processing \'tokenomics\' command: {error}')
        return ERROR_MESSAGES['default'], None


def nft(): #done FC
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F47E FatPunk Collection', callback_data='nft', url=LINKS['nft'])
        btn_b = types.InlineKeyboardButton('\U0001F9C1 Frosting Avatar Collection', callback_data='nft_2', url=LINKS['nft_2'])
        btn_c = types.InlineKeyboardButton('\U0001F430 Rowdy Rabbits Collection', callback_data='rowdy_nft', url=LINKS['rowdy_nft'])
        markup.add(btn_a)
        markup.add(btn_b)
        markup.add(btn_c)
        resp_msg = '\U00002139 Check out our NFT Collections!'
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'nft\' command: {error}')
        return ERROR_MESSAGES['default'], None
 
 
def whitepaper(): #done
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('📑 F.A.T. Ecosystem White Paper',
                                           callback_data='whitepaper',
                                           url=LINKS['whitepaper'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Check out our White Paper'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'whitepaper\' command: {error}')
        return ERROR_MESSAGES['default'], None

 
def merch(): #done FC
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F455 Merch Store',
                                           callback_data='merch',
                                           url=LINKS['merch'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Check out our Fatcake / Frosting Merch Store'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'merch\' command: {error}')
        return ERROR_MESSAGES['default'], None


def channels():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_usa = types.InlineKeyboardButton('🇺🇸 English', callback_data='usa', url=LINKS['usa'])
        btn_china = types.InlineKeyboardButton('\U0001F1E8\U0001F1F3 China', callback_data='china', url=LINKS['china'])
        btn_germany = types.InlineKeyboardButton('\U0001F1E9\U0001F1EA Germany', callback_data='germany', url=LINKS['germany'])
        btn_japan = types.InlineKeyboardButton('\U0001F1EF\U0001F1F5 Japan', callback_data='japan', url=LINKS['japan'])
        btn_india = types.InlineKeyboardButton('\U0001F1EE\U0001F1F3 India', callback_data='india', url=LINKS['india'])
        btn_italian = types.InlineKeyboardButton('\U0001F1EE\U0001F1F9 Italia', callback_data='italian', url=LINKS['italian'])
        btn_arab = types.InlineKeyboardButton('\U0001F3F4 Arab', callback_data='arab', url=LINKS['arab'])
        btn_spain = types.InlineKeyboardButton('\U0001F1EA\U0001F1F8 Spain', callback_data='spain', url=LINKS['spain'])
        markup.add(btn_usa, btn_china),
        markup.add(btn_india, btn_japan),
        markup.add(btn_italian, btn_arab),
        markup.add(btn_spain, btn_germany)

        resp_msg = f'''\U00002139 International Telegram Groups!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'channels\' command: {error}')
        return ERROR_MESSAGES['default'], None


def marketing(): #done FC
    try:
        resp_msg = f'''\U00002139 Please direct all marketing proposals and promotions to \U0001F449 https://t.me/fatpromo.'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'marketing\' command: {error}')
        return ERROR_MESSAGES['default']


def hashtags(): #done FC
    try:
        resp_msg = f'''Primary Hashtags:\n#FATCAKE #FrostingSocial #FATPUNK @FATCAKEtoken\n\nSecondary Hashtags:\n#BinanceSmartChain #BSCGems #BSCGem #BSC #Cryptocurrency #cryptomoonshots #CMS #CAKE #PancakeSwap #rewardcakecoin @PancakeSwap @binance @cz\_binance @elonmusk'''
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'hashtags\' command: {error}')
        return ERROR_MESSAGES['default']


def frosting(): #done FC
    try:
        resp_msg = f'''FAT Ecosystem is launching the world’s first decentralized social media platform.\n\nAnyone can make a channel and charge their users subscription fees, sell NFT’s, live stream and accept anonymous donations!\n\nThis will be a hit for influencers and musicians! Especially since all the revenue gets rewarded to token holders!\n\nRevenue generated by the three apps, ad revenue and two games will be put into the liquidity pool or distributed to the holders in cake rewards, which will boost the price and rewards generating volume adding to the normal volume already generated from the buying and selling of tokens.'''
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'frosting\' command: {error}')
        return ERROR_MESSAGES['default']


def fetch_holders():
    try:
        scraper = cloudscraper.create_scraper()
        req = scraper.get(LINKS['bscscan']).text
        soup = BeautifulSoup(req, 'html.parser')
        div = soup.find_all('div', class_='mr-3')
        holdersResponse = div[0].get_text().split(' ')[0]
        return holdersResponse
    except Exception as error:
        logger.error(f'Error fetching holders: {error}')
        return ERROR_MESSAGES['default']


def fetch_holders_command():
    try:
        holders=fetch_holders()
        resp_msg = f'''\U0001F9C1 FATCAKE Holders: *{holders.strip()}*\n\U00002139 All FatCake holders earn 10% of every transaction based on their percentage of tokens invested.'''
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
            if span.text.split(' ')[1] == 'FATCAKE':
                liq_tokens['FATCAKE'] = span.text.split(' ')[0]
        print(liq_tokens)
        return liq_tokens
    except Exception as error:
        logger.error(f'Error fetching LP tokens: {error}')
        return ERROR_MESSAGES['default']


def fetch_lp():
    try:
        scraper = cloudscraper.create_scraper()
        req = scraper.get(LINKS['bsc_liq']).text
        soup = BeautifulSoup(req, "html.parser")
        div = soup.findAll("div", class_="text-right")
        lp_response = div[0].get_text().split('@')[0]
        return lp_response
    except Exception as error:
        logger.error(f'Error fetching LP: {error}')
        return ERROR_MESSAGES['default']


def price_info():
    try: 
        price_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=fatcake%2Cbinancecoin&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true')
        fat_price_data = price_response.json()
        fat_price = "${:,.8f}".format(fat_price_data['fatcake']['usd'])
        fat_change = int(fat_price_data['fatcake']['usd_24h_change'])
        fat_vol = int(fat_price_data['fatcake']['usd_24h_vol'])
        
        get_marketcap = float((fat_price_data['fatcake']['usd']) * 100000000000)
        marketcap = locale.currency( get_marketcap, grouping=True ).split('.')[0]
        
        bnb_price_data = price_response.json()
        bnb_price = locale.currency( bnb_price_data['binancecoin']['usd'], grouping=True )
        bnb_change = int(bnb_price_data['binancecoin']['usd_24h_change'])
        
        fat_bnb_value = float((bnb_price_data['binancecoin']['usd']) // float(fat_price_data['fatcake']['usd']) * 0.85)
        fat_bnb_dlr_value = locale.currency( fat_bnb_value, grouping=True ).split('$')[1]
        
        holders = fetch_holders()
        
#        liq_tokens = get_liquidity_tokens()
#        bnb_liq_value = float(liq_tokens['WBNB']) * float(bnb_price_data['binancecoin']['usd'])
#        bnb_liq_dlr_value = locale.currency( bnb_liq_value, grouping=True )
#        fat_liq_value = float(liq_tokens['FATCAKE']) * float(fat_price_data['fatcake']['usd'])
#        fat_liq_dlr_value = locale.currency( fat_liq_value, grouping=True )
#        liq_total = locale.currency( (float(bnb_liq_value)) + (float(fat_liq_value)), grouping=True )

        resp_msg = f'''Current price information\n\nName: *FatCake Token*\nSymbol: *FATCAKE*\n\nPrice: *{fat_price} ({fat_change}%) 24H*\n24H Volume: *{fat_vol}*\nMarketcap: *{marketcap}*\nFatCake Holders: *{holders.strip()}*\n\nBNB Price: *{bnb_price} ({bnb_change}%) 24H*\n\n1 BNB = *{fat_bnb_dlr_value} FATCAKE*\n\n'''#\n\nFatCake Liquidity Total: *{liq_total}*\nLiquidity FatCake Qty: *{liq_tokens['FATCAKE']}*\nLiquidity FatCake Value: *{fat_liq_dlr_value}*\nLiquidity BNB Qty: *{liq_tokens['WBNB']}*\nLiquidity BNB Value: *{bnb_liq_dlr_value}*\n\nBNB Price: *{bnb_price} ({bnb_change}%) 24H*'''
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
        
        # TODO - Make parsing of message more robust
        command = get_command_from_body(body)
        if not command:
            logger.info(f'[ INIT - COMMAND ] No command')
            return {
                'statusCode': 200
            }
            
        chat_id = body['message']['chat']['id']
        # username = body['message']['from']['username'] or 'Member'
        
        logger.info('[ INIT ] Validating environment variables')
        for var in ENV_VARS:
            ENV_VARS[var] = os.environ.get(var)
            if ENV_VARS[var] is None:
                raise NameError('Unable to retrieve one or more environment variables')
                
        api_key =  os.environ['telegramApiKey']        
        bot = telebot.TeleBot(api_key, parse_mode='MARKDOWN')        

        if command not in SUPPORTED_COMMANDS:
            logger.info('[ COMMAND ] Unsupported message')
            resp_msg = "Sorry, I don't understand that command, please do /allcommands."
            bot.send_message(chat_id, resp_msg)
            
        if command == 'holders':
            logger.info('[ COMMAND ] Processing /holders request')
            resp_msg = fetch_holders_command()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg)
            
        elif command == 'website':
            logger.info('[ COMMAND ] Processing /website request')
            resp_msg, markup = website()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg, reply_markup=markup)
            
        elif command == 'price_info':
            logger.info('[ COMMAND ] Processing /price_info request')
            resp_msg = price_info()
            bot.send_message(chat_id, resp_msg)
            
        elif command == 'rewards':
            logger.info('[ COMMAND ] Processing /rewards request')
            resp_msg, markup = rewards()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg, reply_markup=markup)
            
        elif command == 'buy':
            logger.info('[ COMMAND ] Processing /buy request')
            resp_msg, markup = buy()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg, reply_markup=markup)
            
        elif command == 'nft':
            logger.info('[ COMMAND ] Processing /nft request')
            resp_msg, markup = nft()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg, reply_markup=markup)
            
        elif command == 'tax':
            logger.info('[ COMMAND ] Processing /tax request')
            resp_msg = tax()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg)
            
        elif command == 'marketing':
            logger.info('[ COMMAND ] Processing /marketing request')
            resp_msg = marketing()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg)
            
        elif command == 'hashtags':
            logger.info('[ COMMAND ] Processing /hashtags request')
            resp_msg = hashtags()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg)
            
        elif command == 'slippage':
            logger.info('[ COMMAND ] Processing /slippage request')
            resp_msg = slippage()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg)
            
        elif command == 'chart' or command == f'charts':
            logger.info('[ COMMAND ] Processing /chart request')
            resp_msg, markup = chart()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg, reply_markup=markup)
            
        elif command == 'contract':
            logger.info('[ COMMAND ] Processing /contract request')
            resp_msg = contract()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg)
            
        elif command == 'bscscan':
            logger.info('[ COMMAND ] Processing /bscscan request')
            resp_msg, markup = bscscan()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg, reply_markup=markup)
            
        elif command == 'liquidity':
            logger.info('[ COMMAND ] Processing /liquidity request')
            resp_msg, markup = liquidity()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg, reply_markup=markup)
            
        elif command == 'allcommands':
            logger.info('[ COMMAND ] Processing /allcommands request')
            resp_msg = allcommands()
            bot.send_message(chat_id, resp_msg)
            
        elif command == 'tokenomics':
            logger.info('[ COMMAND ] Processing /tokenomics request')
            resp_msg, photo = tokenomics()
            bot.send_photo(chat_id, photo, resp_msg)
            
        elif command == 'merch' or command == f'store':
            logger.info('[ COMMAND ] Processing /merch request')
            resp_msg, markup = merch()
            bot.send_photo(chat_id, LINKS['merch_photo'], resp_msg, reply_markup=markup)
            
        elif command == 'channels':
            logger.info('[ COMMAND ] Processing /channels request')
            resp_msg, markup = channels()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg, reply_markup=markup)
            
        elif command == 'whitepaper':
            logger.info('[ COMMAND ] Processing /whitepaper request')
            resp_msg, markup = whitepaper()
            bot.send_photo(chat_id, random.choice(FATCAKE_IMAGES), resp_msg, reply_markup=markup)
            
        elif command == 'frosting':
            logger.info('[ COMMAND ] Processing /frosting request')
            resp_msg = frosting()
            bot.send_photo(chat_id, random.choice(FROSTING_IMAGES), resp_msg)

    except Exception as error:
        logger.error(f'[ FAIL ] Unhandled event: {error}')
        return {
            'statusCode': 200
        }

    return {
        'statusCode': 200
    }