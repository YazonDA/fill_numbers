#!/usr/bin/env python3.6


from modules import *


def main():
	# ==============	Logger Start =============
	logger_format = f'[%(asctime)s] %(levelname)s [%(filename)s/%(funcName)s: %(lineno)d] %(message)s'
	init_logger(logger_format)

	# ==============	Local Data	===============
	'''
	arg_in:
		name of source-file
	return:
		df_4_fill (pandas.dataframe without mistake in all columns
						& ready fo xlsxl-save for fill to Platform)
	'''
	df_4_fill = handling_local(FILE_SOURCE)

	# ==============	DB Data		===============
	'''
	arg_in:
		???
	return:
		???
	'''
	df_4_fill = pd.DataFrame()
	df_4_fill = handling_db(df_4_fill)

	# ==============	The End		===============
	logging.info(f"Logging shutdown\n\n")
	logging.shutdown()
	return 0


if __name__ == '__main__':
	sys.exit(main())
