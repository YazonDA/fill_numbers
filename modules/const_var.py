import os
import sys
import configparser
import logging
import re
import string


def init_config(local_path_config):
	parser = configparser.ConfigParser()
	global_path_config = os.getcwd() + local_path_config
	parser.read(global_path_config)
	
	return parser


def init_logger(l_format, l_config):
	path_logs =	os.getcwd() + l_config['PATH']['logs']
	file_logger = path_logs + l_config['LOGGER']['name_log']
	logging.basicConfig(filename=file_logger,
							format=l_format,
							level=logging.INFO)
	logging.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\nLogging is started!')

def init_files(f_config):
	path_files = os.getcwd() + f_config['PATH']['files']
	
	return path_files + f_config['FILES']['f_source']

def init_columns(c_config):
	cols_source =	c_config['LISTS']['cols_source'	].split('|')
	order_list =	c_config['LISTS']['cols_order'	].split('|')
	add_list =		c_config['LISTS']['cols_add'	].split('|')
	name_list =		c_config['LISTS']['cols_4_fill'	].split('|')
	
	return (cols_source, order_list, add_list, name_list)

def init_4_fill(f_config):
	path_files = os.getcwd() + f_config['PATH']['files']
	
	return path_files + f_config['FILES']['f_4_fill']

def init_repair_dev(c_config):
	path_files = os.getcwd() + c_config['PATH']['files']
	repair_dev_dict = {'ERR_ANCH_QR': c_config['LISTS']['bigQR_list'],
						'FORMAT_BIGQR': r'DevEUI\s{1,}(\S{16})',
						'FORMAT_DEVEUI': r'0016[cC]00000[0-9a-fA-F]{6}',
						'ERR_MSG': 'f',
						'CONST_SEQ': ['x005f', 'x000D'],
						'CONST_RU': 'аАвВсСеЕ',
						'CONST_EN': 'AABBCCEE',
						'CONST_DEVEUI': string.hexdigits,
						'FILE_ERR_OUT': path_files + c_config['FILES']['f_err_out'],
						'PAGE_ERR_DOUBLES': c_config['PAGE_NAME']['err_doubles'],
						'PAGE_ERR_DEV': c_config['PAGE_NAME']['err_dev']}

	return repair_dev_dict


'''
# ==============	Paths		===============

# ==============	File`s Name		===============
FILE_DT = 		path_files + parser['FILES']['f_datetime'	]
FILE_4_REFILL = path_files + parser['FILES']['f_4_refill'	]
FILE_WR_STAT = 	path_files + parser['FILES']['f_wr_stat'	]

# ==============	Page`s Name		===============
PAGE_ERR_RFID =		parser['PAGE_NAME']['err_rfid' 		]
PAGE_ERR_COORD =	parser['PAGE_NAME']['err_coord'		]
PAGE_ERR_ORG =		parser['PAGE_NAME']['err_org'		]
PAGE_ERR_POLE_POSE =parser['PAGE_NAME']['err_pole_pos'	]
PAGE_ERR_ROAD_POSE =parser['PAGE_NAME']['err_road_pos'	]
PAGE_ERR_NOT_MOT =	parser['PAGE_NAME']['err_not_mot'	]
PAGE_ERR_ISIN =		parser['PAGE_NAME']['err_isin'		]







#dict_cols_caption = {'cols_source': cols_source, 'cols_order': cols_order, 'cols_add': cols_add, 'cols_4_fill': cols_4_fill}
DICT_ORG_SECT = dict(zip(parser['LISTS']['org_list'].split('|'), parser['LISTS']['sect_list'].split('|')))
STATUSES = tuple(parser['LISTS']['stat_list'].split('|'))

# sample for some compare
CONST_RFID = string.ascii_letters + string.digits
MINMAX_Y = list(map(float, parser['COORD']['minmax_Y'].split('|')))
MINMAX_X = list(map(float, parser['COORD']['minmax_X'].split('|')))
ROAD_LIST = parser['LISTS']['road_set'].split('|')
POLE_LIST = parser['LISTS']['pole'].split('|')
ERR_FIND_ORG = parser['LISTS']['err_find_org']
ERR_FIND_POS = parser['LISTS']['err_find_pos']
'''




if __name__ == '__main__':
	sys.exit(print('You tried to run this module. But this is only a library.\nNot for independent launch!'))
