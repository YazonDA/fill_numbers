#!/usr/bin/env python3.6


import psycopg2
from psycopg2 import Error
import logging
import sys

from modules import *


def lists_in_dbase():
	try:
		# connect to DB
		connection = psycopg2.connect("dbname='customer_01' user='lorawan' host='pg-db.vms.oug' password='ves2018'")
		# cursor for doing something
		cursor = connection.cursor()
		request_motes = f"SELECT lpad(to_hex(eui), 16, '0') FROM motes;"
		request_lights_true = f"SELECT * FROM lights WHERE (install_user_id IN (SELECT id FROM users WHERE role_id = 4)) OR (pnr_status = 100);"
		request_lights_false = f"SELECT * FROM lights WHERE NOT ((install_user_id IN (SELECT id FROM users WHERE role_id = 4)) OR (pnr_status = 100));"

		cursor.execute(request_motes)
		_list_motes = list(map(lambda x: x[0], cursor.fetchall()))
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

def check_stat(dev_list):
	try:
		# connect to DB
		connection = psycopg2.connect("dbname='customer_01' user='lorawan' host='pg-db.vms.oug' password='ves2018'")
		# cursor for doing something
		cursor = connection.cursor()
		request_motes = f"SELECT lpad(to_hex(eui), 16, '0') FROM motes WHERE status IN {STATUSES} AND lpad(to_hex(eui), 16, '0') IN {tuple(dev_list)};"

		cursor.execute(request_motes)
		_list_motes = list(map(lambda x: x[0], cursor.fetchall()))

		request_motes = f"SELECT lpad(to_hex(eui), 16, '0'), status FROM motes WHERE lpad(to_hex(eui), 16, '0') IN {tuple(dev_list)} AND status NOT IN {STATUSES};"
		cursor.execute(request_motes)
		_list_stats = list(map(lambda x: [x[0], x[1]], cursor.fetchall()))

		return (_list_motes, _list_stats)
	
	except (Exception, Error) as error:
		print("Some error by work with PostgreSQL", error)
	finally:
		if connection:
			cursor.close()
			connection.close()
			logging.info(f"\nConnection to PostgreSQL is closed\n")

def get_table(dev_list):
	try:
		# connect to DB
		connection = psycopg2.connect("dbname='customer_01' user='lorawan' host='pg-db.vms.oug' password='ves2018'")
		# cursor for doing something
		cursor = connection.cursor()
		request_table = f"SELECT \
			lights.modem_dev_eui, poles.latitude, poles.longitude, poles.pole_id_original, poles.rfid, \
			lk_sectors.name, poles.sector_id, street_refs.name, pole_refs.name, poles.lamp_marks, \
			poles.okrug_municipal, poles.okrug_adm, poles.street, poles.pole_orientir \
			FROM lights \
			JOIN poles \
			ON poles.pole_id = lights.pole_id \
			JOIN pole_refs \
			ON pole_refs.ref_id=poles.ref_id \
			JOIN street_refs \
			ON street_refs.ref_id=poles.street_ref_id \
			JOIN lk_sectors \
			ON lk_sectors.pk_sector_id=poles.sector_id \
			WHERE lights.modem_dev_eui IN {tuple(dev_list)};"

		cursor.execute(request_table)
		_list_motes = list(cursor.fetchall())

		return _list_motes
	
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
	logging.info(f'it`s completed!\n\
		not_motes == {len(_df_err_not_motes)}\n\
		in_lights_true == {len(_df_err_in_lights_true)}\n\
		in_lights_false == {len(_df_err_in_lights_false)}\n\
		4_fill == {len(_df_4_fill)}')

	return (_df_err_not_motes, _df_err_in_lights_true, _df_err_in_lights_false, _df_4_fill)


if __name__ == '__main__':
	sys.exit(print('You are maked attempt to run this module. But it`s only libraries. Not for run!'))
