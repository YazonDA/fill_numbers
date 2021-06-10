#!/usr/bin/env python3

import sys
import logging
import logging.config
import configparser
import os
import string

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

# List of some  Column`s Names
cols_order = ['QR код контроллера', 'Координата Х WGS84', 'Координата Y WGS84', 'ID опоры', 'RFID значение метки на опоре', 'Организация', 'N сектора', '№ ШУНО', 'Положение светильника относительно дороги', 'Положение светильника на опоре', 'Марки светильников, установленных на опоре (БД Моссвет)', 'Муниципальный округ (БД Моссвет)', 'Административный округ (БД Моссвет)', 'Улица (БД Моссвет)', 'Ориентир (БД Моссвет)']
cols_add = ['N сектора', '№ ШУНО']
cols_rename = ['DevEUI', 'Координата Y WGS84, широта', 'Координата Х WGS84, долгота', 'ID опоры', 'RFID значение метки на опоре', 'Сектор / Организация', 'N сектора', '№ ШУНО', 'Положение светильника относительно дороги', 'Положение светильника на опоре', 'Марки светильников, установленных на опоре (БД Моссвет)', 'Муниципальный округ (БД Моссвет)', 'Административный округ (БД Моссвет)', 'Улица (БД Моссвет)', 'Ориентир (БД Моссвет)']


# sample for some compare
#const_dev = string.hexdigits
const_ru = 'аАвВсСеЕ'
const_en = 'AABBCCEE'
const_seq = ['x005f', 'x000D']
const_hex = string.hexdigits

# ============== SET LOGGER ===============


line_format = "[%(asctime)s] %(levelname)s [%(funcName)s: %(lineno)d] %(message)s"

logging.basicConfig(filename=file_log,
						format=line_format,
						level=logging.INFO)

# ============== MAIN ===============

def main():
	'''
	print(check_bigQR('DevEUI  0016c00000114fbc; AppEUI 00-06-00-01-00-00-00-07; AppKey  ; DevAddr  00-11-4f-bc; AppSKey 45:13:65:86:72:5a:a1:0c:bc:09:ac:f7:01:21:4b:4e; NwkSEncKey 8c:4c:c2:31:3c:57:27:14:23:53:51:44:40:66:8a:02; FNwkSIntKey  f5:66:62:38:8a:01:f5:8f:a7:a2:3a:26:08:f1:c7:65; SNwkSIntKey '))

	return 0
	#'''
	logging.info('Module is started!')

	df_4_fill = read_xlsx(file_source)

	df_4_fill = columns_add(df_4_fill, cols_add)
	df_4_fill = columns_order(df_4_fill, cols_order)
	df_4_fill = columns_rename(df_4_fill, cols_rename)

	list_deveui = df_4_fill['DevEUI'].tolist()

	list_deveui_1 = repair_cells(list_deveui)


	write_xlsx(df_4_fill, file_4_fill)

	logging.info(f"Logging shutdown\n\n")
	logging.shutdown()
	return 0


if __name__ == '__main__':
	sys.exit(main())

