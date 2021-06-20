import os
import configparser
import logging
import string
import re


# ============== SET CONSTANTs & VARIABLES e.t.c.===============

# some Paths
path_main = os.getcwd() + '/'

path_set = path_main + 'setup/settings.ini'
parser = configparser.ConfigParser()
parser.read(path_set)

path_log = path_main + parser["PATH"]["logs"]
path_modul = path_main + parser["PATH"]["modules"]
path_file = path_main + parser["PATH"]["files"]

# SET LOGGER
FILE_LOGGER = path_log + 'tmp_log'
LOGGER_FORMAT = "[%(asctime)s] %(levelname)s [%(funcName)s: %(lineno)d] %(message)s"
logging.basicConfig(filename=FILE_LOGGER,
						format=LOGGER_FORMAT,
						level=logging.INFO)
logging.info('Logging is started!')

# Names of some Files
file_source = path_file + parser['FILES']['f_source']
FILE_ERR_OUT = path_file + parser['FILES']['f_err_out']
FILE_4_FILL = path_file + parser['FILES']['f_4_fill']

ERR_MSG='f'

# Names of some Pages (in xlsx)
PAGE_ERR_DEV =		parser['PAGE_NAME']['err_dev']
PAGE_ERR_RFID =		parser['PAGE_NAME']['err_rfid']
PAGE_ERR_COORD =	parser['PAGE_NAME']['err_coord']
PAGE_ERR_DOUBLES =	parser['PAGE_NAME']['err_doubles']
PAGE_ERR_ORG =		parser['PAGE_NAME']['err_org']
PAGE_ERR_NOT_MOT =	parser['PAGE_NAME']['err_not_mot']
PAGE_ERR_ISIN =		parser['PAGE_NAME']['err_isin']

# List of some Column`s Names
COLS_SOURCE = parser['LISTS']['cols_source'].split('|')
ORDER_LIST = parser['LISTS']['cols_order'].split('|')
ADD_LIST = parser['LISTS']['cols_add'].split('|')
NAME_LIST = parser['LISTS']['cols_4_fill'].split('|')
#dict_cols_caption = {'cols_source': cols_source, 'cols_order': cols_order, 'cols_add': cols_add, 'cols_4_fill': cols_4_fill}
DICT_ORG_SECT = dict(zip(parser['LISTS']['org_list'].split('|'), parser['LISTS']['sect_list'].split('|')))

# sample for some compare
CONST_RU = 'аАвВсСеЕ'
CONST_EN = 'AABBCCEE'
CONST_SEQ = ['x005f', 'x000D']
CONST_DEVEUI = string.hexdigits
CONST_RFID = string.ascii_letters + string.digits
FORMAT_DEVEUI = r'0016[cC]00000[0-9a-fA-F]{6}'
MINMAX_Y = list(map(float, parser['COORD']['minmax_Y'].split('|')))
MINMAX_X = list(map(float, parser['COORD']['minmax_X'].split('|')))

