BOT_NAME = 'Stock Bot'
API_URL = 'https://stooq.com/q/l/?s=%s&f=sd2t2ohlcv&h&e=csv'
STOCK_CODE = {'prefix': 'stock', 'name': 'Stock'}
BOT_CODES = {STOCK_CODE['prefix']: STOCK_CODE}
USER_ERROR_COMMAND = 'Error on command'
MESSAGE_ERROR_COMMAND = 'The format of your command is incorrect, correct it and try again'
MESSAGE_EMPTY_COMMAND = 'Command response is empty, try with other value'
EMPTY_VALUE = 'N/D'
