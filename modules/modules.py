#!/usr/bin/env python3.6


import pandas as pd
import logging
import string
import re
import csv
import sys

from modules import *


#---01---
# Block for working with some files ------------------------------
def read_xlsx(filename):
	# special for XLSX
	try:
		array = pd.read_excel(filename, engine='openpyxl')
		logging.info(f'{filename.split("/")[-1]} == {len(array)} lines; it`s completed!')
		return array
	except (FileNotFoundError, IsADirectoryError):
		logging.error(f'FileNotFoundError, IsADirectoryError')
		exit(1)

def write_new_xlsx(in_df, filename, pagename=''):
	# special for XLSX
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
	# for all non-xlsx
	arr = []
	with open(filename, 'r') as csv_file:
		reader = csv.reader(csv_file, dialect = 'excel')
		for i in reader:
			if choice_key:
				i[0] = '00' + i[0]
			arr.append(*i)
	logging.info(f'{filename.split("/")[-1]} == {len(arr)} lines; it`s completed!')
	return arr
#---01------------------------------------------------------------

#---02---
# Block for working with some columns & captions -----------------
def col_name_ord(in_df):
		# columns_order
		in_df = in_df.reindex(columns=ORDER_LIST)
		# columns_rename
		in_df.columns = NAME_LIST
		return in_df

def columns_repair(in_df, flag_datetime=False):
	# check format/names in dataframe
	if list(in_df.columns) == NAME_LIST:
		return in_df # coz not need 'repaire'
	elif list(in_df.columns) == COLS_SOURCE:
		# columns_add
		for col_name in ADD_LIST:
			in_df[col_name] = 0

		#>>>>>
		# ATTENTION!!! it`s a temporary solution!!!
		# not in here! not this logic!
		if flag_datetime:
			ORDER_LIST.append('Дата внесения изменения')
			NAME_LIST.append('Дата ОЭК')
			#logging.info(f'\nORDER_LIST\n{ORDER_LIST},\n NAME_LIST\n{NAME_LIST}')
		#<<<<<

		return col_name_ord(in_df) 

	return False

#---02------------------------------------------------------------

def split_doubles(in_df, col_name):
	df_doubles = in_df[in_df.duplicated(subset=col_name, keep=False)]
	df_N_doubles = in_df.drop_duplicates(subset=col_name, keep=False)
	logging.info('it`s completed!')
	return df_doubles, df_N_doubles

def re_index(in_df):
	tmp_new_ind = list(range(len(in_df)))
	in_df['tmp_new_ind'] = tmp_new_ind
	in_df = in_df.set_index('tmp_new_ind')
	logging.info('it`s completed!')
	return in_df

def check_rus(deveui):
	try:
		for tmp_rus in CONST_RU:
			if tmp_rus in deveui:
				return ''.join(CONST_EN[CONST_RU.index(chr)] if (chr in CONST_RU) else chr for chr in deveui)
		return deveui
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "ffffffff"')
		return ERR_MSG

def check_seq(deveui):
	try:
		for seq in CONST_SEQ:
			while seq in deveui:
				deveui = deveui[:deveui.index(seq)] + deveui[deveui.index(seq) + len(seq):]
		return deveui
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "ffffffff"')
		return ERR_MSG

def check_hex(deveui):
	try:
		zzz = ''.join(i for i in deveui if i in CONST_DEVEUI)
		if len(zzz) == 0:
			return ERR_MSG
		return zzz
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "ffffffff"')
		return ERR_MSG

def check_dec(rfid):
	try:
		zzz = ''.join(i for i in rfid if i in CONST_RFID)
		if len(zzz) == 0:
			return ERR_MSG
		return zzz
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "ffffffff"')
		return ERR_MSG

def check_bigQR(deveui, anch=ERR_ANCH_QR):
	try:
		if anch in deveui:
			return (re.match(FORMAT_BIGQR, deveui)).group(1)
		return deveui 
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "ffffffff"')
		return ERR_MSG
	except (AttributeError):
		#logging.error(f'AttributeError: dev == {deveui}')
		return ERR_MSG

def repair_dev(deveui_list):
	answer = []
	for deveui in deveui_list:
		deveui = check_bigQR(deveui)
		deveui = check_seq(deveui)
		deveui = check_rus(deveui)
		deveui = check_hex(deveui)
		answer.append(deveui.lower())
	logging.info('it`s completed!')
	return answer

def mask_deveui(deveui_list):
	mask = []
	for deveui in deveui_list:
		mask.append(bool(re.fullmatch(FORMAT_DEVEUI, deveui)))
	logging.info('it`s completed!')
	return mask

def repair_rfid(rfid_list):
	answer = []
	for rfid in rfid_list:
		zzz = check_seq(rfid)
		zzz = check_dec(zzz)
		answer.append(zzz)
	logging.info('it`s completed!')
	return answer

def mask_rfid(rfid_list):
	mask = []
	for rfid in rfid_list:
		mask.append(bool(len(rfid) >= 6))
	logging.info('it`s completed!')
	return mask

def check_coord(coord_list, minmax):
	mask = []
	for ind, coord in enumerate(coord_list):
		if isinstance(coord, str):
			if re.match(r'^\d{2},\d{4,}$', coord):
				coord_list[ind] = float(coord.replace(',', '.'))
				coord = coord_list[ind]
		if isinstance(coord, float):
			mask.append(bool(minmax[0] <= coord <= minmax[1]))
			continue
		mask.append(False)
	logging.info('it`s completed!')
	return coord_list, mask

def repair_org(org_list):
	n_sect_list = []
	for ind in range(len(org_list)):
		if org_list[ind] not in DICT_ORG_SECT:
			org_list[ind] = ERR_FIND_ORG
		n_sect_list.append(DICT_ORG_SECT[org_list[ind]])
	logging.info('it`s completed!')
	return (org_list, n_sect_list)

def repair_pole_road(in_list, comp_list):
	n_sect_list = []
	for ind in range(len(in_list)):
		if in_list[ind] not in comp_list:
			in_list[ind] = ERR_FIND_POS
	logging.info('it`s completed!')
	return in_list


if __name__ == '__main__':
	sys.exit(print('You are maked attempt to run this module. But it`s only libraries. Not for run!'))