import pandas as pd
import logging
	

class xlsx():
	pass

def read_xlsx(filename):
	# special for XLSX
	#logging.info('into READ_XLSX')
	array = []
	try:
		array = pd.read_excel(filename)
		logging.info(f'Length == {len(array)}\nModule is completed!')
		return array
	except (FileNotFoundError, IsADirectoryError):
		logging.error(f'FileNotFoundError, IsADirectoryError')
		exit(1)

def write_xlsx(in_df, filename):
	# special for XLSX
	in_df.to_excel(filename, index=False)
	logging.info(f'Length == {len(in_df)}\nModule is completed!')

def columns_add(in_df, add_list):
	for col_name in add_list:
		in_df[col_name] = 0
	logging.info('Module is completed!')
	return in_df

def columns_order(in_df, order_list, len=15):
	in_df = in_df.reindex(columns=order_list)
	logging.info('Module is completed!')
	return in_df

def columns_rename(in_df, name_list):
	in_df.columns = name_list
	#cols = list(tmp_df.columns.values)
	logging.info('Module is completed!')
	return in_df

def columns_list(in_df):
	return list(in_df.columns.values)

if __name__ == '__main__':
	print(f'You are make attempt to run this module.\n\
		But it`s only libraries. Not for run!')
	#sys.exit(print('OK!'))