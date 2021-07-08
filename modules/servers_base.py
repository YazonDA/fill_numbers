#!/usr/bin/env python3.6


import psycopg2
from psycopg2 import Error
import logging
import sys

from modules import *


def lists_in_dbase():
	try:
		# connect to DB
		connection = psycopg2.connect("dbname='customer_01' user='lorawan' host='localhost' password='ves2018'")
		# cursor for doing something
		cursor = connection.cursor()
		request_motes = f"SELECT lpad(to_hex(eui), 16, '0') FROM motes;"
		request_lights = f"SELECT modem_dev_eui FROM lights;"
		request_lights_true = f"SELECT * FROM lights WHERE (install_user_id IN (SELECT id FROM users WHERE role_id = 4)) OR (pnr_status = 100);"
		request_lights_false = f"SELECT * FROM lights WHERE NOT ((install_user_id IN (SELECT id FROM users WHERE role_id = 4)) OR (pnr_status = 100));"

		cursor.execute(request_motes)
		_list_motes = list(map(lambda x: x[0], cursor.fetchall()))
		#cursor.execute(request_lights)
		#_list_lights = list(map(lambda x: x[0], cursor.fetchall()))
		cursor.execute(request_lights_true)
		_list_lights_true = list(map(lambda x: x[0], cursor.fetchall()))
		cursor.execute(request_lights_false)
		_list_lights_false = list(map(lambda x: x[0], cursor.fetchall()))
		logging.info('it`s completed!')
		return (_list_lights_true, _list_lights_false, _list_motes)
	
	except (Exception, Error) as error:
		print("Some error by work with PostgreSQL", error)
	finally:
		if connection:
			cursor.close()
			connection.close()
			logging.info(f"\nConnection to PostgreSQL is closed\n")
	
def lists_in_dbase_from_file(_file_db_lights, _file_db_motes):
	_list_lights = modules.read_csv(_file_db_lights)
	_list_motes = modules.read_csv(_file_db_motes, True)
	logging.info('it`s completed!')
	return (_list_lights, _list_motes)

def motes_no_lights(_df_4_fill, _file_db_lights=0, _file_db_motes=0):
	#_list_lights, _list_motes = lists_in_dbase_from_file(_file_db_lights, _file_db_motes)	
	_list_lights_true, _list_lights_false, _list_motes = lists_in_dbase()
	
	_df_err_not_motes = _df_4_fill[~_df_4_fill['DevEUI'].isin(_list_motes)]
	_df_4_fill = _df_4_fill[_df_4_fill['DevEUI'].isin(_list_motes)]
	_df_err_in_lights_true = _df_4_fill[_df_4_fill['DevEUI'].isin(_list_lights_true)]
	_df_4_fill = _df_4_fill[~_df_4_fill['DevEUI'].isin(_list_lights_true)]
	_df_err_in_lights_false = _df_4_fill[_df_4_fill['DevEUI'].isin(_list_lights_false)]
	_df_4_fill = _df_4_fill[~_df_4_fill['DevEUI'].isin(_list_lights_false)]
	logging.info(f'it`s completed!\nnot_motes == {len(_df_err_not_motes)}\nin_lights == {len(_df_err_in_lights)}\n4_fill == {len(_df_4_fill)}')

	return (_df_err_not_motes, _df_err_in_lights_true, _df_err_in_lights_false, _df_4_fill)


if __name__ == '__main__':
	sys.exit(print('You are maked attempt to run this module. But it`s only libraries. Not for run!'))
