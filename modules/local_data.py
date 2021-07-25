#!/usr/bin/env python3.6

from modules.in_out import *
from modules import *

def handling_local(in_file):
	logging.info(f'Module is started!\nFile_source is:\n{in_file}')
	tmp_df = read_xlsx(in_file)
	logging.info(f'Module will return this file:\n{len(tmp_df)} rows; {type(tmp_df)}')
	return tmp_df

if __name__ == '__main__':
	sys.exit(print('You are maked attempt to run this module. But it`s only libraries. Not for run!'))