#!/usr/bin/env python3.6


import sys
import logging
import pandas as pd


def handling_local(my_config):
	import modules.in_out as fio
	import modules.columns as cols
	import modules.const_var as const_var
	
	logging.info(f'Module is started!\n')

	name_source = const_var.init_files(my_config)
	logging.info(f'File_source is:\n{name_source}')
	
	tmp_df = fio.read_xlsx(name_source)
	if not isinstance(tmp_df, pd.DataFrame):
		print(f'Source-file is not a class pandas.core.frame.DataFrame !')
		logging.error(f'Unknow format of source-file!')
		exit(1)

	tmp_df = tmp_df.fillna('')

	tmp_df = cols.name_and_order(tmp_df, my_config)
	if not isinstance(tmp_df, pd.DataFrame):
		print(f'Unknow format of columns in source-file!')
		logging.error(f'Unknow format of columns in source-file!')
		exit(1)

	logging.info(f'Module will return this DF:\n{len(tmp_df)} rows; {type(tmp_df)}')
	
	return tmp_df

def work_is_done(in_df, my_config):
	import modules.in_out as fio
	import modules.const_var as const_var
	name_4_fill = const_var.init_4_fill(my_config)

	fio.write_new_xlsx(in_df, name_4_fill)

	logging.info(f"Logging shutdown\n\n")
	logging.shutdown()

if __name__ == '__main__':
	sys.exit(print('You tried to run this module. But this is only a library.\nNot for independent launch!'))
