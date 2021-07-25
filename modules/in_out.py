#!/usr/bin/env python3.6

'''
import pandas as pd
import logging
import string
import re
import csv
import sys
'''
from modules import *


def read_xlsx(filename):
	try:
		array = pd.read_excel(filename, engine='openpyxl')
		logging.info(f'{filename.split("/")[-1]} == {len(array)} lines; it`s completed!')
		return array
	except (FileNotFoundError, IsADirectoryError):
		logging.error(f'FileNotFoundError, IsADirectoryError')
		exit(1)

def write_new_xlsx(in_df, filename, pagename=''):
	if pagename == '':
		pagename = 'NoName'
	in_df.to_excel(filename, index=False, sheet_name=pagename)
	logging.info(f'{filename.split("/")[-1]} page {pagename} == {len(in_df)} lines; it`s completed!')

def write_page_xlsx(in_df, filename, pagename):
	# special for existing XLSX
	with pd.ExcelWriter(filename, mode='a') as ex_writer:
		in_df.to_excel(ex_writer, sheet_name=pagename, index=False)
	logging.info(f'{filename.split("/")[-1]} page {pagename} == {len(in_df)} lines; it`s completed!')

def write_csv(arr, filename):
	with open(filename, 'w') as csv_file:
		writer = csv.writer(csv_file, dialect = 'excel')
		for i in arr:
			writer.writerow([i])
	logging.info(f'{filename.split("/")[-1]} == {len(arr)} lines; it`s completed!')
	return True

def read_csv(filename, choice_key=False):
	arr = []
	with open(filename, 'r') as csv_file:
		reader = csv.reader(csv_file, dialect = 'excel')
		for i in reader:
			if choice_key:
				i[0] = '00' + i[0]
			arr.append(*i)
	logging.info(f'{filename.split("/")[-1]} == {len(arr)} lines; it`s completed!')
	return arr


if __name__ == '__main__':
	sys.exit(print('You are maked attempt to run this module. But it`s only libraries. Not for run!'))