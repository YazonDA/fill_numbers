#!/usr/bin/env python3

import sys
import logging
#import logging.config
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
#file_source = path_file + 'tst_f_source.xlsx' # THIS IS TEMPORARY! THEN REMOVE!
file_4_fill = path_file + parser['FILES']['f_4_fill']
#file_4_fill = path_file + 'tst_f_4_fill.xlsx'  # THIS IS TEMPORARY! THEN REMOVE!
file_4_pass = path_file + parser['FILES']['f_4_pass']
file_err_dev = path_file + parser['FILES']['f_err_dev']
file_err_rfid = path_file + parser['FILES']['f_err_rfid']
file_err_coord = path_file + parser['FILES']['f_err_coord']
file_doubles = path_file + parser['FILES']['f_doubles']
file_org = path_file + parser['FILES']['f_org']

# List of some  Column`s Names
cols_order = parser['LISTS']['cols_order'].split('|')
cols_add = parser['LISTS']['cols_add'].split('|')
cols_rename = parser['LISTS']['cols_rename'].split('|')
dict_org_sect = dict(zip(parser['LISTS']['org_list'].split('|'), parser['LISTS']['sect_list'].split('|')))

# sample for some compare
#const_dev = string.hexdigits
const_ru = 'аАвВсСеЕ'
const_en = 'AABBCCEE'
const_seq = ['x005f', 'x000D']
const_deveui = string.hexdigits
const_rfid = string.ascii_letters + string.digits
format_deveui = r'0016[cC]00000[0-9a-fA-F]{6}'
minmax_Y = list(map(float, parser['COORD']['minmax_Y'].split('|')))
minmax_X = list(map(float, parser['COORD']['minmax_X'].split('|')))

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

	# 1--
	# Сохранить Файл-источник, как Файл-добавлений.
	# Поменять местами, удалить не нужные и переименовать столбцы
	df_4_fill = read_xlsx(file_source)
	df_4_fill = columns_add(df_4_fill, cols_add)
	df_4_fill = columns_order(df_4_fill, cols_order)
	df_4_fill = columns_rename(df_4_fill, cols_rename)
	#-1---------------------------------------------------------------
	
	# 2--
	# Обработать колонку DevEUI
	list_deveui = df_4_fill['DevEUI'].tolist()
	list_repaired_deveui = repair_dev(list_deveui)
	mask_dev = pd.Series(mask_deveui(list_repaired_deveui))
	df_err_dev = df_4_fill[~mask_dev]
	df_4_fill['DevEUI'] = list_repaired_deveui
	df_4_fill = df_4_fill[mask_dev]
	
	write_xlsx(df_err_dev, file_err_dev)
	write_xlsx(df_4_fill, file_4_fill)
	# w/o this string -- Error ... and I don`t know why :(
	df_4_fill = read_xlsx(file_4_fill)
	#-----------------------------------------------------------------

	list_deveui = df_4_fill['DevEUI'].tolist()
	mask_doub = pd.Series(mask_double(list_deveui))
	df_doubles = df_4_fill[~mask_doub]
	df_4_fill = df_4_fill[mask_doub]

	write_xlsx(df_doubles, file_doubles)
	write_xlsx(df_4_fill, file_4_fill)
	#-2---------------------------------------------------------------

	# 3--
	# Обработать колонку RFID
	df_4_fill = read_xlsx(file_4_fill)
	list_rfid = df_4_fill['RFID значение метки на опоре'].tolist()
	list_repaired_rfid = repair_rfid(list_rfid)
	
	mask_rf = pd.Series(mask_rfid(list_repaired_rfid))
	df_err_rfid = df_4_fill[~mask_rf]
	df_4_fill['RFID значение метки на опоре'] = list_repaired_rfid
	df_4_fill = df_4_fill[mask_rf]
	
	write_xlsx(df_err_rfid, file_err_rfid)
	write_xlsx(df_4_fill, file_4_fill)
	#-3---------------------------------------------------------------

	# 4--
	# Обработать колонки Координата
	df_4_fill = read_xlsx(file_4_fill)
	list_coord_Y = df_4_fill['Координата Y WGS84, широта'].tolist()
	list_coord_X = df_4_fill['Координата Х WGS84, долгота'].tolist()
	
	list_coord_Y_rep, mask_coord_Y = check_coord(list_coord_Y, minmax_Y)
	list_coord_X_rep, mask_coord_X = check_coord(list_coord_X, minmax_X)
	
	if False in mask_coord_X or False in mask_coord_Y:
		mask_coord = pd.Series(list(map(lambda x, y: x and y, mask_coord_X, mask_coord_Y)))
		logging.info('split by coord_err')
		df_err_coord = df_4_fill[~mask_coord]
		df_4_fill['Координата Y WGS84, широта'] = list_coord_Y_rep
		df_4_fill['Координата Х WGS84, долгота'] = list_coord_X_rep
		df_4_fill = df_4_fill[mask_coord]
		write_xlsx(df_err_coord, file_err_coord)

	write_xlsx(df_4_fill, file_4_fill)
	#-4---------------------------------------------------------------
	
	# 5--
	# Обработать колонки Сектор / Организация & N сектора
	df_4_fill = read_xlsx(file_4_fill)
	list_org = df_4_fill['Сектор / Организация'].tolist()
	list_org_rep, list_n_sect = repair_org(list_org, dict_org_sect)
	df_4_fill['Сектор / Организация'] = list_org_rep
	df_4_fill['N сектора'] = list_n_sect

	write_xlsx(df_4_fill, file_4_fill)
	#-5---------------------------------------------------------------


	logging.info(f"Logging shutdown\n\n")
	logging.shutdown()
	return 0


if __name__ == '__main__':
	sys.exit(main())

