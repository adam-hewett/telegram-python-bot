#Crow Finance

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

import boto3
s3 = boto3.resource('s3')

# Environment Variables
ENV_VARS = {
    'telegramApiKey': '',
    'BOT_NAME': ''
}

LINKS = {
    'crow-cro': 'https://dexscreener.com/cronos/0xcd693f158865d071f100444c7f3b96e7463bae8d',
    'crow-usdc': 'https://dexscreener.com/cronos/0x82e623aa112b03388a153d51142e5f9ea7ece258'
}

ERROR_MESSAGES = {
    'default': 'Sorry, an error occurred processing your request, wait a few seconds and try again.'
}

SUPPORTED_COMMANDS = [
    'allcommands',
    'price',
    'price1h',
    'price4h',
    'price1d'
]

EXCLUDED_COMMANDS = [
#    'prices'
    # 'price'
]

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

        markup = types.InlineKeyboardMarkup()
        btn_cro = types.InlineKeyboardButton('$CROW / $CRO Chart', callback_data='chart', url=LINKS['crow-cro'])
        btn_usdc = types.InlineKeyboardButton('$CROW / $USDC Chart', callback_data='chart', url=LINKS['crow-usdc'])
        markup.add(btn_cro)
        markup.add(btn_usdc)
            
        if command == 'price' or command == 'price1h':
            logger.info('[ COMMAND ] Processing /price request')
            logger.info('Getting file from s3')
            s3.meta.client.download_file('price-processor', 'crow-finance.png', '/tmp/crow-finance.png')
            s3.meta.client.download_file('price-processor', 'crow-finance.txt', '/tmp/crow-finance.txt')
            logger.info('file downloaded')
            resp_msg = ''
            with open('/tmp/crow-finance.txt') as f:
                resp_msg = f.read()
            bot.send_photo(chat_id, open('/tmp/crow-finance.png', 'rb'), resp_msg, reply_markup=markup)
        elif command == 'price4h':
            logger.info('[ COMMAND ] Processing /price4h request')
            logger.info('Getting file from s3')
            s3.meta.client.download_file('price-processor', 'crow-finance-4h.png', '/tmp/crow-finance-4h.png')
            s3.meta.client.download_file('price-processor', 'crow-finance.txt', '/tmp/crow-finance.txt')
            logger.info('file downloaded')
            resp_msg = ''
            with open('/tmp/crow-finance.txt') as f:
                resp_msg = f.read()
                resp_msg = resp_msg.replace('Current price information with 1 hour chart', 'Current price information with 4 hour chart')
            bot.send_photo(chat_id, open('/tmp/crow-finance-4h.png', 'rb'), resp_msg, reply_markup=markup)
        elif command == 'price1d':
            logger.info('[ COMMAND ] Processing /price1d request')
            logger.info('Getting file from s3')
            s3.meta.client.download_file('price-processor', 'crow-finance-1d.png', '/tmp/crow-finance-1d.png')
            s3.meta.client.download_file('price-processor', 'crow-finance.txt', '/tmp/crow-finance.txt')
            logger.info('file downloaded')
            resp_msg = ''
            with open('/tmp/crow-finance.txt') as f:
                resp_msg = f.read()
                resp_msg = resp_msg.replace('Current price information with 1 hour chart', 'Current price information with 1 day chart')
            bot.send_photo(chat_id, open('/tmp/crow-finance-1d.png', 'rb'), resp_msg, reply_markup=markup)
        
    except Exception as error:
        logger.error(f'[ FAIL ] Unhandled event: {error}')
        return {
            'statusCode': 200
        }

    return {
        'statusCode': 200
    }