#!/usr/bin/env python3.6


import sys
import logging
import configparser

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

		print(in_df.columns)

		# columns_order
		in_df = in_df.reindex(columns=ORDER_LIST)
		# columns_rename
		in_df.columns = NAME_LIST

		return in_df
	return False


if __name__ == '__main__':
	sys.exit(print('You tried to run this module. But this is only a library.\nNot for independent launch!'))
