#!/usr/bin/env python3.6


import sys
import logging


def handling_local(in_file):
	import modules.in_out as fio
	import modules.columns as cols
	
	logging.info(f'Module is started!\nFile_source is:\n{in_file}')
	
	tmp_df = fio.read_xlsx(in_file)
	
	logging.info(f'Module will return this file:\n{len(tmp_df)} rows; {type(tmp_df)}')
	
	return tmp_df

if __name__ == '__main__':
	sys.exit(print('You tried to run this module. But this is only a library.\nNot for independent launch!'))