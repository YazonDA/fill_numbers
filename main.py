#!/usr/bin/env python3.6


import os
from modules import *


# ============== MAIN ===============

def main():
	logging.info('Main-Module is started!')
	
	# 1--
	df_4_fill = read_xlsx(file_source)
	if not isinstance(df_4_fill, pd.DataFrame):
		print(f'It`s not a class pandas.core.frame.DataFrame !')
		logging.error(f'Unknow format of columns in source-file!')
		return 1
	
	# 5.1--
	# create dict for dev/app pairs
	list_4_dev = df_4_fill['DevEUI'].tolist()
	tuple_4_dev = list(set(list_4_dev))
	list_couples = get_table(tuple_4_dev)

	#-5.1-------------------------------------------------------------
	
	# 13--
	# Записать финальный файл для заливки номеров
	write_new_xlsx(df_4_fill, FILE_4_FILL)
	#-13---------------------------------------------------------------


	logging.info(f"Logging shutdown\n\n")
	logging.shutdown()
	return 0


if __name__ == '__main__':
	sys.exit(main())
