#!/usr/bin/env python3.6


from modules import *


def main():
	# ==============	Create Parser =============
	path_config = '/setup/settings.ini'
	my_config = init_config(path_config)

	# ==============	Logger Start =============
	logger_format = f'\n\t[%(asctime)s] %(levelname)s\n[%(filename)s\t\t%(funcName)s: %(lineno)d]\n%(message)s'
	init_logger(logger_format, my_config)

	# ==============	Local Data	===============
	'''
	arg_in:
		name of source-file
	return:
		df_4_fill (pandas.dataframe without mistake in all columns
						& ready fo xlsxl-save for fill to Platform)
	'''
	df_4_fill = handling_local(my_config)

	# ==============	DB Data		===============
	'''
	arg_in:
		???
	return:
		???
	'''
	df_4_fill = handling_db(df_4_fill)

	# ==============	The End		===============
	work_is_done(df_4_fill, my_config)
	return 0


if __name__ == '__main__':
	sys.exit(main())
