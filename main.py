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

	tmp_name = path_file + 'tst_f_source.xlsx'
	tmp_df = read_xlsx(tmp_name)

	tmp_df = columns_add(tmp_df, cols_add)
	tmp_df = columns_order(tmp_df, cols_order)
	tmp_df = columns_rename(tmp_df, cols_rename)

	write_xlsx(tmp_df, path_file + 'tst_f_4_fill.xlsx')

	logging.info(f"Logging shutdown\n\n")
	logging.shutdown()
	return 0


if __name__ == '__main__':
	sys.exit(main())

