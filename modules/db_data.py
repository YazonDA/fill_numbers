#!/usr/bin/env python3.6


import sys
import logging


def handling_db(df_in):
	logging.info(f'Module is started!\nin_DF is:\n{len(df_in)} rows; {type(df_in)}')
	return df_in

if __name__ == '__main__':
	sys.exit(print('You tried to run this module. But this is only a library.\nNot for independent launch!'))