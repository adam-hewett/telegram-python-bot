#SeaChainToken

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

NAME = 'SeaChain Token'
SYMBOL = 'SeaChain'
CONTRACT_ADDRESS = '0x36b24b2f78725495e858af9e72f7df69dade3dca'
LP_CONTRACT_ADDRESS = '0x74b1c9fe9b0cb0a395dc76acb00de288939682a1'
SUPPLY = '600000000000'

ERROR_MESSAGES = {
    'default': 'Sorry, an error occurred processing your request, wait a few seconds and try again.'
}

LINKS = {


    'rewards': f'https://trackbsc.com/earnings?token={CONTRACT_ADDRESS}',
    'rewards_photo': 'https://i.ibb.co/sVfTVpG/seachainbanner.png',
#    'dapp': 'https://trackbsc.com/portfolio',
#    'dapp_photo': 'https://i.ibb.co/K59pkBd/Portfolio-Tracker.jpg',

    'medium': 'https://seachaintoken.medium.com',
    'medium_photo': 'https://i.ibb.co/NrzKPMm/Medium.png',
    
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
        resp_msg = f'''\U00002139 Here are all commands!\n\n/website\n/contract\n/buy\n/holders\n/chart\n/price\n/rewards\n/mediumarticles\n/tokenomics\n/groups'''
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'allcommands\' command: {error}')
        return ERROR_MESSAGES['default']

def rewards():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F449 Track Your Rewards \U0001F448',
                                           callback_data='rewards',
                                           url=LINKS['rewards'])
        markup.add(btn_a)
        resp_msg = f'''\n\U00002139 Check {SYMBOL} reflection rewards on TrackBSC.com!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'rewards\' command: {error}')
        return ERROR_MESSAGES['default'], None


def mediumarticles():
    try:
        markup = types.InlineKeyboardMarkup()
        btn_a = types.InlineKeyboardButton('\U0001F4F0 Medium Articles.',
                                           callback_data='medium_articles',
                                           url=LINKS['medium'])
        markup.add(btn_a)
        resp_msg = f'''\U00002139 Get the latest updates from our Medium Articles!'''
        return resp_msg, markup
    except Exception as error:
        logger.error(f'Error occurred processing \'medium_articles\' command: {error}')
        return ERROR_MESSAGES['default'], None


def tokenomics():
    try:
        resp_msg = f'\U00002139 Each SeaChain network transaction incurs a 10% Tax.\n├ 5% Redistributed To Holders\n├ 2% Funding & Development\n├ 1% Community Governed Wallet\n├ 1% Locked Liquidity Pool\n└ 1% Marketing & Promotion'
        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'tokenomics\' command: {error}')
        return ERROR_MESSAGES['default']


def slippage():
    try:
        resp_msg = f'''\n\n\U00002139 Set slippage to minimum 10% on [Apeswap](https://app.apeswap.finance/swap?outputCurrency=0x36b24b2f78725495e858af9e72f7df69dade3dca).'''
        return resp_msg
    except Exception as error:
        logger.error(
            f'Error occurred processing \'slippage\' command: {error}')
        return ERROR_MESSAGES['default']


def groups():
    try:
        resp_msg = f'''
{NAME} Official Groups

🌐Chat Groups
├🇺🇸 @SeaChainNetwork
├🇳🇱 @SeaChainTokenNetherlands
├🇮🇩 @SeaChainTokenIndonesia
├🇹🇷 @SeaChainTokenTurkey
├🇵🇹🇧🇷 @SeaChainBrasilPortugal
└🇷🇺🇺🇦 @seachain\_rus\_ukr

📣 Shill Group
└ @SeaChainShillingArmy

🗞 News
└ @SeaChainTokenAnnouncements

💬SeaChain Migration Support 
└@PangeaOceanClean
'''

        return resp_msg
    except Exception as error:
        logger.error(f'Error occurred processing \'channels\' command: {error}')
        return ERROR_MESSAGES['default'], None


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

        elif command == 'rewards':
            logger.info('[ COMMAND ] Processing /rewards request')
            resp_msg, markup = rewards()
            bot.send_photo(chat_id, LINKS['rewards_photo'], resp_msg, reply_markup=markup)
#            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
#        elif command == 'dapp' or command == f'app':
#            logger.info('[ COMMAND ] Processing /dapp request')
#            resp_msg, markup = dapp()
#            bot.send_photo(chat_id, LINKS['dapp_photo'], resp_msg, reply_markup=markup)
#            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
        elif command == 'mediumarticles':
            logger.info('[ COMMAND ] Processing /mediumarticles request')
            resp_msg, markup = mediumarticles()
            bot.send_photo(chat_id, LINKS['medium_photo'], resp_msg, reply_markup=markup)
#            bot.send_message(chat_id, resp_msg, reply_markup=markup)
            
        elif command == 'tokenomics':
            logger.info('[ COMMAND ] Processing /tokenomics request')
            resp_msg = tokenomics()
            bot.send_message(chat_id, resp_msg)
            
        elif command == 'groups':
            logger.info('[ COMMAND ] Processing /groups request')
            resp_msg = groups()
            bot.send_message(chat_id, resp_msg)
        
    except Exception as error:
        logger.error(f'[ FAIL ] Unhandled event: {error}')
        return {
            'statusCode': 200
        }

    return {
        'statusCode': 200
    }