from django.utils import timezone

from utils.constants import STOCK_CODE, BOT_CODES, USER_ERROR_COMMAND, MESSAGE_ERROR_COMMAND
from utils.request_api import get_csv_response_api
from django.utils.translation import gettext_lazy as _

from utils.utils import get_date_with_template_format


def is_bot_message(message):
    for code in BOT_CODES.values():
        if is_prefix_bot_message(message, code['prefix']):
            return True
    return False


def format_prefix(prefix):
    return '/%s=' % prefix


def is_prefix_bot_message(message, prefix):
    parts = message.split(' ')
    if len(parts) == 1:
        if message.startswith(format_prefix(prefix)):
            parts_code = message.split('=')
            return len(parts_code) == 2 and parts_code[1] != ''
    return False


def get_prefix_from_message(message):
    return message[1:].split('=')[0]


def get_name_code_from_message(message):
    return BOT_CODES[get_prefix_from_message(message)]['name']


def process_message_with_stock_code(message):
    stock_code = message.replace(format_prefix(STOCK_CODE['prefix']), '')
    rows_csv = get_csv_response_api(stock_code)
    row_data = rows_csv[1]
    open_data = row_data[3]
    return _('%s quote is $%s per share') % (stock_code.upper(), open_data)


def process_bot_message(message):
    codes = {STOCK_CODE['prefix']: process_message_with_stock_code}
    prefix = get_prefix_from_message(message)
    return prefix, codes[prefix](message)


def error_bot_response():
    return {
        'user_to_show': str(_(USER_ERROR_COMMAND)),
        'message': str(_(MESSAGE_ERROR_COMMAND)),
        'creation_date': get_date_with_template_format(timezone.now)
    }
