#!/usr/bin/env python3.6


import psycopg2
from psycopg2 import Error
import logging
import sys

import modules

def print_string(st_01, st_02):
	print('{}\t{}'.format(st_01, st_02))

def lists_in_dbase():
	try:
		# connect to DB
		connection = psycopg2.connect("dbname='customer_01' user='lorawan' host='localhost' password='ves2018'")

		# cursor for doing something
		cursor = connection.cursor()

		request_motes = f'SELECT to_hex(eui) FROM motes;'
		request_lights = f'SELECT modem_dev_eui FROM lights;'

		cursor.execute(request_motes)
		_list_motes = cursor.fetchall()
		cursor.execute(request_lights)
		_list_lights = cursor.fetchall()
		return (_list_lights, _list_motes)
		logging.info(f'RETURN isn`t working')

	except (Exception, Error) as error:
		print("Some error by work with PostgreSQL", error)
	finally:
		if connection:
			cursor.close()
			connection.close()
			logging.info(f"\nConnection to PostgreSQL is closed\n")
			#return (_list_lights, _list_motes)

def lists_in_dbase_from_file(_file_db_lights, _file_db_motes):
	_list_lights = modules.read_csv(_file_db_lights)
	_list_motes = modules.read_csv(_file_db_motes, True)
	logging.info('it`s completed!')
	return (_list_lights, _list_motes)

def motes_no_lights(_df_4_fill, _file_db_lights, _file_db_motes):
	logging.info(f'_df_4_fill {len(_df_4_fill)} , {type(_df_4_fill)}')
	#_list_lights, _list_motes = lists_in_dbase_from_file(_file_db_lights, _file_db_motes)	
	_list_lights, _list_motes = lists_in_dbase_()
	logging.info(f'return from lists_in_dbase (_list_lights, _list_motes)')
	logging.info(f'_list_lights {len(_list_lights)}, _list_motes {len(_list_motes)}')

	_df_err_not_motes = _df_4_fill[~_df_4_fill['DevEUI'].isin(_list_motes)]
	_df_4_fill = _df_4_fill[_df_4_fill['DevEUI'].isin(_list_motes)]
	_df_err_in_lights = _df_4_fill[_df_4_fill['DevEUI'].isin(_list_lights)]
	_df_4_fill = _df_4_fill[~_df_4_fill['DevEUI'].isin(_list_lights)]
	logging.info('it`s completed!')
	logging.info(f'\nnot_motes == {len(_df_err_not_motes)}, in_lights == {len(_df_err_in_lights)}, 4_fill == {len(_df_4_fill)}')
	return (_df_err_not_motes, _df_err_in_lights, _df_4_fill)


if __name__ == '__main__':
	sys.exit(print('You are make attempt to run this module. But it`s only libraries. Not for run!'))
