#!/usr/bin/env python3.6


import sys
import logging
import configparser
import re
import pandas as pd
import modules.in_out as f_io

def re_index(in_df):
	tmp_new_ind = list(range(len(in_df)))
	in_df['tmp_new_ind'] = tmp_new_ind
	in_df = in_df.set_index('tmp_new_ind')
	logging.info('it`s completed!')
	return in_df

def name_and_order(in_df, in_config):
	logging.info(f'Module is started!\n')
	import modules.const_var as const_var
	COLS_SOURCE, ORDER_LIST, ADD_LIST, NAME_LIST = const_var.init_columns(in_config)
	
	# check format/names in dataframe
	if list(in_df.columns) == NAME_LIST:
		return in_df # coz not need 'repaire'

	elif list(in_df.columns) == COLS_SOURCE:
		# columns_add
		for col_name in ADD_LIST:
			in_df[col_name] = 0

		# columns_order
		in_df = in_df.reindex(columns=ORDER_LIST)
		# columns_rename
		in_df.columns = NAME_LIST

		logging.info(f'Module will return this DF:\n{len(in_df)} rows; {type(in_df)}')
		return in_df
	return False

def repair_column(in_df, name_col):
	return in_df

def check_hex(deveui, repair_dev_dict):
	try:
		zzz = ''.join(i for i in deveui if i in repair_dev_dict['CONST_DEVEUI'])
		if len(zzz) == 0:
			return repair_dev_dict['ERR_MSG']
		return zzz
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "f"')
		return repair_dev_dict['ERR_MSG']

def check_digits(rfid, repair_dev_dict):
	try:
		zzz = ''.join(i for i in rfid if i in repair_dev_dict['CONST_RFID'])
		if len(zzz) == 0:
			return repair_dev_dict['ERR_MSG']
		return zzz
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "f"')
		return repair_dev_dict['ERR_MSG']

def check_rus(deveui, repair_dev_dict):
	try:
		for tmp_rus in repair_dev_dict['CONST_RU']:
			if tmp_rus in deveui:
				return ''.join(repair_dev_dict['CONST_EN'][repair_dev_dict['CONST_RU'].index(chr)] if (chr in repair_dev_dict['CONST_RU']) else chr for chr in deveui)
		return deveui
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "f"')
		return repair_dev_dict['ERR_MSG']

def check_seq(deveui, repair_dev_dict):
	try:
		for seq in repair_dev_dict['CONST_SEQ']:
			while seq in deveui:
				deveui = deveui[:deveui.index(seq)] + deveui[deveui.index(seq) + len(seq):]
		return deveui
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "f"')
		return repair_dev_dict['ERR_MSG']

def check_bigQR(deveui, repair_dev_dict):
	anch=repair_dev_dict['ERR_ANCH_QR']
	try:
		if anch in deveui:
			return (re.match(repair_dev_dict['FORMAT_BIGQR'], deveui)).group(1)
		return deveui 
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "f"')
		return repair_dev_dict['ERR_MSG']
	except (AttributeError):
		#logging.error(f'AttributeError: dev == {deveui}')
		return repair_dev_dict['ERR_MSG']

def split_doubles(in_df, col_name):
	df_doubles = in_df[in_df.duplicated(subset=col_name, keep=False)]
	df_N_doubles = in_df.drop_duplicates(subset=col_name, keep=False)
	logging.info('it`s completed!')
	return df_doubles, df_N_doubles

def repair_dev(in_df, repair_dev_dict):
	logging.info(f'Module is started!\n')

	# prepare file for error_pages
	f_io.write_new_xlsx(pd.DataFrame(), repair_dev_dict['FILE_ERR_OUT'])

	columns_name = 'DevEUI'
	rule_of_mask = repair_dev_dict['all_mask'][columns_name]
	list_deveui = in_df[columns_name].tolist()

	answer = []
	for deveui in list_deveui:
		deveui = check_bigQR(deveui, repair_dev_dict)
		deveui = check_seq(deveui, repair_dev_dict)
		deveui = check_rus(deveui, repair_dev_dict)
		deveui = check_hex(deveui, repair_dev_dict)
		answer.append(deveui.lower())
	
	mask = get_mask(answer, rule_of_mask)
	if False in mask:
		mask = pd.Series(mask)
		

		df_err_dev = in_df[~mask]
		
		in_df[columns_name] = answer
		in_df = in_df[mask]
		in_df = re_index(in_df)
	
		f_io.write_page_xlsx(df_err_dev, repair_dev_dict['FILE_ERR_OUT'], repair_dev_dict['PAGE_ERR_DEV'])

	df_err_doubles, in_df = split_doubles(in_df, columns_name)
	in_df = re_index(in_df)

	f_io.write_page_xlsx(df_err_doubles, repair_dev_dict['FILE_ERR_OUT'], repair_dev_dict['PAGE_ERR_DOUBLES'])
	
	logging.info('it`s completed!')
	return in_df

def get_mask(in_list, in_rule):
	'''
	in_list -- list of column`s values (dev, rfid, etc). from def_repair_
	in_rule -- special lambda for each column 
	'''
	mask = []

	for piece in in_list:
		mask.append(in_rule(piece))

	logging.info(f'it`s completed!')
	return mask

def repair_rfid(in_df, repair_dev_dict):
	logging.info(f'Module is started!\n')
	
	columns_name = 'RFID значение метки на опоре'
	rule_of_mask = repair_dev_dict['all_mask'][columns_name]
	list_rfid = in_df[columns_name].tolist()
	
	answer = []
	for rfid in list_rfid:
		rfid = check_seq(rfid, repair_dev_dict)
		rfid = check_digits(rfid, repair_dev_dict)
		answer.append(rfid)

	#mask = pd.Series(mask_rfid(answer, repair_dev_dict))
	mask = pd.Series(get_mask(answer, rule_of_mask))

	df_err_rfid = in_df[~mask]
	
	in_df[columns_name] = answer
	in_df = in_df[mask]
	in_df = re_index(in_df)
	
	f_io.write_page_xlsx(df_err_rfid, repair_dev_dict['FILE_ERR_OUT'], repair_dev_dict['PAGE_ERR_RFID'])
	
	logging.info('it`s completed!')
	return in_df

if __name__ == '__main__':
	sys.exit(print('You tried to run this module. But this is only a library.\nNot for independent launch!'))
