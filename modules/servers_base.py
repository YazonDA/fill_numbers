#!/usr/bin/env python3.6


import psycopg2
from psycopg2 import Error
import logging
import sys

from modules import *


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
