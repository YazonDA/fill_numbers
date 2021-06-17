#!/usr/bin/env python3.6


import psycopg2
from psycopg2 import Error
import modules
import logging
import sys

def print_string(st_01, st_02):
	print('{}\t{}'.format(st_01, st_02))

def list_in_dbase():
	try:
		# connect to DB
		connection = psycopg2.connect("dbname='customer_01' user='lorawan' host='localhost' password='ves2018'")

		# cursor for doing something
		cursor = connection.cursor()

		string_1 = 'count'
		string_2 = 'status'

		my_query = f'SELECT to_hex(m.eui) FROM motes m LEFT JOIN lights l ON (m.eui = l.modem_dev_eui_dec);'
		cursor.execute(my_query)

		result = cursor.fetchall()
		return result

	except (Exception, Error) as error:
		print("Some error by work with PostgreSQL", error)
	finally:
		if connection:
			cursor.close()
			connection.close()
			print("\nConnection to PostgreSQL is closed\n")

def list_in_dbase_from_file(filename):
	result = modules.read_csv(filename, True)
	return result

def motes_no_lights(_df_4_fill, _file_db_lights, _file_db_motes):
	_list_lights = modules.read_csv(_file_db_lights)
	_list_motes = modules.read_csv(_file_db_motes, True)
	
	_df_err_not_motes = _df_4_fill[~_df_4_fill['DevEUI'].isin(_list_motes)]
	_df_4_fill = _df_4_fill[_df_4_fill['DevEUI'].isin(_list_motes)]
	_df_err_in_lights = _df_4_fill[_df_4_fill['DevEUI'].isin(_list_lights)]
	_df_4_fill = _df_4_fill[~_df_4_fill['DevEUI'].isin(_list_lights)]
	logging.info(f'(not_motes == {len(_df_err_not_motes)}, in_lights == {len(_df_err_in_lights)}, 4_fill == {len(_df_4_fill)})')
	return (_df_err_not_motes, _df_err_in_lights, _df_4_fill)


if __name__ == '__main__':
	sys.exit(print('You are make attempt to run this module. But it`s only libraries. Not for run!'))
