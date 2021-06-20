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

# ============== SET LOGGER ===============
FILE_LOGGER = path_log + 'tmp_log'
LOGGER_FORMAT = "[%(asctime)s] %(levelname)s [%(funcName)s: %(lineno)d] %(message)s"
logging.basicConfig(filename=FILE_LOGGER,
						format=LOGGER_FORMAT,
						level=logging.INFO)
logging.info('Logging is started!')

# Names of some Files
file_source = path_file + parser['FILES']['f_source']
file_err_out = path_file + parser['FILES']['f_err_out']
try:
	zzz = os.system(f'cp {file_source} {file_err_out}')
	if zzz:
		raise FileNotFoundError('\ncan`t to find file named {file_source}')
	logging.info(f'file_source is finded & copied')
except (FileNotFoundError, IsADirectoryError):
	logging.error(f'FileNotFoundError, IsADirectoryError')
	exit(1)



FILE_4_FILL = path_file + parser['FILES']['f_4_fill']

# Names of some Pages (in xlsx)
PAGE_ERR_DEV =		parser['PAGE_NAME']['err_dev']
PAGE_ERR_RFID =		parser['PAGE_NAME']['err_rfid']
PAGE_ERR_COORD =	parser['PAGE_NAME']['err_coord']
PAGE_ERR_DOUBLES =	parser['PAGE_NAME']['err_doubles']
PAGE_ERR_ORG =		parser['PAGE_NAME']['err_org']
PAGE_ERR_NOT_MOT =	parser['PAGE_NAME']['err_not_mot']
PAGE_ERR_ISIN =		parser['PAGE_NAME']['err_isin']

# List of some Column`s Names
cols_source = parser['LISTS']['cols_source'].split('|')
cols_order = parser['LISTS']['cols_order'].split('|')
cols_add = parser['LISTS']['cols_add'].split('|')
cols_4_fill = parser['LISTS']['cols_4_fill'].split('|')
dict_cols_caption = {'cols_source': cols_source, 'cols_order': cols_order, 'cols_add': cols_add, 'cols_4_fill': cols_4_fill}
dict_org_sect = dict(zip(parser['LISTS']['org_list'].split('|'), parser['LISTS']['sect_list'].split('|')))

# sample for some compare
const_ru = 'аАвВсСеЕ'
const_en = 'AABBCCEE'
const_seq = ['x005f', 'x000D']
const_deveui = string.hexdigits
const_rfid = string.ascii_letters + string.digits
format_deveui = r'0016[cC]00000[0-9a-fA-F]{6}'
minmax_Y = list(map(float, parser['COORD']['minmax_Y'].split('|')))
minmax_X = list(map(float, parser['COORD']['minmax_X'].split('|')))

