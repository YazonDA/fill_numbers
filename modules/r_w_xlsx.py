import pandas as pd


def read_xlsx(filename):
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

#print(__name__)
'''
if __name__ == '__main__':
	sys.exit(print('OK!'))
'''