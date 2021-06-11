#!/usr/bin/env python3

import sys
import logging
import logging.config
import configparser
import os
import string
import re

from modules import *

# ============== SET CONSTANTs & VARIABLES ===============

# Names of some Paths
path_main = os.getcwd() + '/'

path_set = path_main + 'setup/settings.ini'
parser = configparser.ConfigParser()
parser.read(path_set)

path_log = path_main + parser["PATH"]["logs"]
path_modul = path_main + parser["PATH"]["modules"]
path_file = path_main + parser["PATH"]["files"]

# Names of some Files
file_log = path_log + 'tmp_log'
file_source = path_file + parser['FILES']['f_source']
file_source = path_file + 'tst_f_source.xlsx' # THIS IS TEMPORARY! THEN REMOVE!
file_4_fill = path_file + parser['FILES']['f_4_fill']
file_4_fill = path_file + 'tst_f_4_fill.xlsx'  # THIS IS TEMPORARY! THEN REMOVE!
file_4_pass = path_file + parser['FILES']['f_4_pass']
file_err_dev = path_file + parser['FILES']['f_err_dev']
file_err_rfid = path_file + parser['FILES']['f_err_rfid']
file_err_coord = path_file + parser['FILES']['f_err_coord']
file_doubles = path_file + parser['FILES']['f_doubles']

# List of some  Column`s Names
cols_order = parser['LISTS']['cols_order'].split('|')
cols_add = parser['LISTS']['cols_add'].split('|')
cols_rename = parser['LISTS']['cols_rename'].split('|')


# sample for some compare
#const_dev = string.hexdigits
const_ru = 'аАвВсСеЕ'
const_en = 'AABBCCEE'
const_seq = ['x005f', 'x000D']
const_deveui = string.hexdigits
const_rfid = string.ascii_letters + string.digits
format_deveui = r'0016[cC]00000[0-9a-fA-F]{6}'

# ============== SET LOGGER ===============


line_format = "[%(asctime)s] %(levelname)s [%(funcName)s: %(lineno)d] %(message)s"

logging.basicConfig(filename=file_log,
						format=line_format,
						level=logging.INFO)

# ============== MAIN ===============

def main():
	'''
	print(cols_order, '\n', type(cols_order))
	for i in cols_order:
		print(i)
	return 0
	#'''
	logging.info('Module is started!')

	df_4_fill = read_xlsx(file_source)

	df_4_fill = columns_add(df_4_fill, cols_add)
	df_4_fill = columns_order(df_4_fill, cols_order)
	df_4_fill = columns_rename(df_4_fill, cols_rename)

	list_deveui = df_4_fill['DevEUI'].tolist()
	list_repaired_deveui = repair_dev(list_deveui)
	
	mask_dev = pd.Series(mask_deveui(list_repaired_deveui))
	df_err_dev = df_4_fill[~mask_dev]
	df_4_fill['DevEUI'] = list_repaired_deveui
	df_4_fill = df_4_fill[mask_dev]

	# w/o this two string of code -- Error ... and I don`t know why :(
	write_xlsx(df_4_fill, file_4_fill)
	df_4_fill = read_xlsx(file_4_fill)

	list_deveui = df_4_fill['DevEUI'].tolist()
	mask_doub = pd.Series(mask_double(list_deveui))
	df_doubles = df_4_fill[~mask_doub]
	df_4_fill = df_4_fill[mask_doub]

	write_xlsx(df_err_dev, file_err_dev)
	write_xlsx(df_doubles, file_doubles)

	list_rfid = df_4_fill['RFID значение метки на опоре'].tolist()
	list_repaired_rfid = repair_rfid(list_rfid)

	# w/o this two string of code -- Error ... and I don`t know why :(
	write_xlsx(df_4_fill, file_4_fill)
	df_4_fill = read_xlsx(file_4_fill)
	
	mask_rf = pd.Series(mask_rfid(list_repaired_rfid))
	df_err_rfid = df_4_fill[~mask_rf]
	df_4_fill['RFID значение метки на опоре'] = list_repaired_rfid
	df_4_fill = df_4_fill[mask_rf]
	
	write_xlsx(df_4_fill, file_4_fill)
	write_xlsx(df_err_rfid, file_err_rfid)

	logging.info(f"Logging shutdown\n\n")
	logging.shutdown()
	return 0


if __name__ == '__main__':
	sys.exit(main())

