#!/usr/bin/env python3

import sys
import logging
import logging.config
import configparser
import os

from modules import *

# ============== SET CONSTANTs & VARIABLES ===============

path_main = os.getcwd() + '/'

path_set = path_main + 'setup/settings.ini'
parser = configparser.ConfigParser()
parser.read(path_set)

path_log = path_main + parser["PATH"]["logs"]
path_modul = path_main + parser["PATH"]["modules"]
path_file = path_main + parser["PATH"]["files"]

file_log = path_log + 'tmp_log'
file_source = path_file + parser['FILES']['f_source']
file_source = path_file + 'tst_f_source.xlsx' # THIS IS TEMPORARY! THEN REMOVE!
file_4_fill = path_file + parser['FILES']['f_4_fill']
file_4_fill = path_file + 'tst_f_4_fill.xlsx'  # THIS IS TEMPORARY! THEN REMOVE!
file_4_pass = path_file + parser['FILES']['f_4_pass']
file_err_dev = path_file + parser['FILES']['f_err_dev']
file_err_rfid = path_file + parser['FILES']['f_err_rfid']
file_err_coord = path_file + parser['FILES']['f_err_coord']


cols_order = ['QR код контроллера', 'Координата Х WGS84', 'Координата Y WGS84', 'ID опоры', 'RFID значение метки на опоре', 'Организация', 'N сектора', '№ ШУНО', 'Положение светильника относительно дороги', 'Положение светильника на опоре', 'Марки светильников, установленных на опоре (БД Моссвет)', 'Муниципальный округ (БД Моссвет)', 'Административный округ (БД Моссвет)', 'Улица (БД Моссвет)', 'Ориентир (БД Моссвет)']
cols_add = ['N сектора', '№ ШУНО']
cols_rename = ['DevEUI', 'Координата Y WGS84, широта', 'Координата Х WGS84, долгота', 'ID опоры', 'RFID значение метки на опоре', 'Сектор / Организация', 'N сектора', '№ ШУНО', 'Положение светильника относительно дороги', 'Положение светильника на опоре', 'Марки светильников, установленных на опоре (БД Моссвет)', 'Муниципальный округ (БД Моссвет)', 'Административный округ (БД Моссвет)', 'Улица (БД Моссвет)', 'Ориентир (БД Моссвет)']

# ============== SET LOGGER ===============


line_format = "[%(asctime)s] %(levelname)s [%(funcName)s: %(lineno)d] %(message)s"

logging.basicConfig(filename=file_log,
						format=line_format,
						level=logging.INFO)

# ============== MAIN ===============

def main():
	logging.info('Module is started!')

	df_4_fill = read_xlsx(file_source)

	df_4_fill = columns_add(df_4_fill, cols_add)
	df_4_fill = columns_order(df_4_fill, cols_order)
	df_4_fill = columns_rename(df_4_fill, cols_rename)

	write_xlsx(df_4_fill, file_4_fill)

	logging.info(f"Logging shutdown\n\n")
	logging.shutdown()
	return 0


if __name__ == '__main__':
	sys.exit(main())

