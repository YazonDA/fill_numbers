import os
import sys
import configparser
import logging
import pandas as pd


# ==============	Paths		===============
path_main = os.getcwd() + '/'

path_settings = path_main + 'setup/settings.ini'
parser = configparser.ConfigParser()
parser.read(path_settings)

path_logs = path_main + parser['PATH']['logs']
path_modul = path_main + parser['PATH']['modules']
path_files = path_main + parser['PATH']['files']

# ==============	File`s Name	===============
FILE_SOURCE = path_files + parser['FILES']['f_source']
FILE_DT = path_files + parser['FILES']['f_datetime']
FILE_ERR_OUT = path_files + parser['FILES']['f_err_out']
FILE_4_FILL = path_files + parser['FILES']['f_4_fill']
FILE_4_REFILL = path_files + parser['FILES']['f_4_refill']
FILE_WR_STAT = path_files + parser['FILES']['f_wr_stat']

# ==============	Page`s Name	===============
PAGE_ERR_DEV =		parser['PAGE_NAME']['err_dev']
PAGE_ERR_RFID =		parser['PAGE_NAME']['err_rfid']
PAGE_ERR_COORD =	parser['PAGE_NAME']['err_coord']
PAGE_ERR_DOUBLES =	parser['PAGE_NAME']['err_doubles']
PAGE_ERR_ORG =		parser['PAGE_NAME']['err_org']
PAGE_ERR_POLE_POSE =parser['PAGE_NAME']['err_pole_pos']
PAGE_ERR_ROAD_POSE =parser['PAGE_NAME']['err_road_pos']
PAGE_ERR_NOT_MOT =	parser['PAGE_NAME']['err_not_mot']
PAGE_ERR_ISIN =		parser['PAGE_NAME']['err_isin']


def init_logger(logger_format):
	# set Logger
	FILE_LOGGER = path_logs + parser['LOGGER']['name_log']
	LOGGER_FORMAT = logger_format
	logging.basicConfig(filename=FILE_LOGGER,
							format=LOGGER_FORMAT,
							level=logging.INFO)
	logging.info('Logging is started!')


'''

ERR_MSG='f'


# List of some Column`s Names
COLS_SOURCE = parser['LISTS']['cols_source'].split('|')
ORDER_LIST = parser['LISTS']['cols_order'].split('|')
ADD_LIST = parser['LISTS']['cols_add'].split('|')
NAME_LIST = parser['LISTS']['cols_4_fill'].split('|')
#dict_cols_caption = {'cols_source': cols_source, 'cols_order': cols_order, 'cols_add': cols_add, 'cols_4_fill': cols_4_fill}
DICT_ORG_SECT = dict(zip(parser['LISTS']['org_list'].split('|'), parser['LISTS']['sect_list'].split('|')))
STATUSES = tuple(parser['LISTS']['stat_list'].split('|'))

# sample for some compare
CONST_RU = 'аАвВсСеЕ'
CONST_EN = 'AABBCCEE'
CONST_SEQ = ['x005f', 'x000D']
CONST_DEVEUI = string.hexdigits
CONST_RFID = string.ascii_letters + string.digits
FORMAT_DEVEUI = r'0016[cC]00000[0-9a-fA-F]{6}'
FORMAT_BIGQR = r'DevEUI\s{1,}(\S{16})'
MINMAX_Y = list(map(float, parser['COORD']['minmax_Y'].split('|')))
MINMAX_X = list(map(float, parser['COORD']['minmax_X'].split('|')))
ROAD_LIST = parser['LISTS']['road_set'].split('|')
POLE_LIST = parser['LISTS']['pole'].split('|')
ERR_FIND_ORG = parser['LISTS']['err_find_org']
ERR_FIND_POS = parser['LISTS']['err_find_pos']
ERR_ANCH_QR = parser['LISTS']['bigQR_list']
'''




if __name__ == '__main__':
	sys.exit(print('You tried to run this module. But this is only a library.\nNot for independent launch!'))
