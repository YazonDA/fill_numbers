import pandas as pd
import logging
#import logging.config

#import modules

#logger = logging.getLogger("read_xlsx")
	

class xlsx():
	pass

def read_xlsx(filename):
	#logger.info('into READ_XLSX')
	logging.info('into READ_XLSX')
	# special for XLSX
	array = []
	try:
		array = pd.read_excel(filename)
		return array
	except (FileNotFoundError, IsADirectoryError):
		logging.error(f'FileNotFoundError, IsADirectoryError')
		exit(1)

def write_xlsx(in_df, filename):
	# special for XLSX
	in_df.to_excel(filename, index=False)

def ppprint():
	logging.info('msg13')

if __name__ == '__main__':
	print(f'You are make attempt to run this module.\n\
		But it`s only libraries. Not for run!')
	#sys.exit(print('OK!'))