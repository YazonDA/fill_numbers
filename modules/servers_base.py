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
		connection = psycopg2.connect("dbname='customer_01' user='lorawan' host='localhost' password='ves2018'")
		# cursor for doing something
		cursor = connection.cursor()
		request_motes = f"SELECT lpad(to_hex(eui), 16, '0') FROM motes WHERE status IN {STATUSES};"

		cursor.execute(request_motes)
		_list_motes = list(map(lambda x: x[0], cursor.fetchall()))

		request_motes = f"SELECT lpad(to_hex(eui), 16, '0'), status FROM motes WHERE lpad(to_hex(eui), 16, '0') IN {tuple(dev_list)};"
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
		connection = psycopg2.connect("dbname='customer_01' user='lorawan' host='localhost' password='ves2018'")
		# cursor for doing something
		cursor = connection.cursor()
		request_table = f"SELECT\
							lpad(to_hex(eui), 16, '0'), lpad(to_hex(appeui), 16, '0')\
							FROM motes\
							WHERE lpad(to_hex(eui), 16, '0') IN {tuple(dev_list)};"

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


if __name__ == '__main__':
	sys.exit(print('You are maked attempt to run this module. But it`s only libraries. Not for run!'))
