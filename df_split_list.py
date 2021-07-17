import pandas as pd
import csv
import sys


FILE_DIR = f'/home/yda/prgr/fill_numbers/files/res_20210715/'
SOURCE_NAME = FILE_DIR + f'f_wrong_stat.xlsx'
WRONG_NAME = FILE_DIR + f'from_serg.csv'
OUT_NAME = FILE_DIR + 'refill_after_serg.xlsx'

def f_read_csv(filename):
	arr = []
	with open(filename, 'r') as csv_file:
		reader = csv.reader(csv_file, dialect = 'excel')
		for i in reader:
			arr.append(*i)
	print(f'{filename.split("/")[-1]} == {len(arr)} lines; csv_read is completed!')
	return arr

def f_read_xlsx(filename):
	try:
		_df_out = pd.read_excel(filename, engine='openpyxl')
		print(f'{filename.split("/")[-1]} == {len(_df_out)} lines; xlsx_read is completed!')
		return _df_out
	except (FileNotFoundError, IsADirectoryError):
		logging.error(f'FileNotFoundError, IsADirectoryError')
		exit(1)

def f_write_xlsx(in_df, filename, pagename=''):
	# special for XLSX
	if pagename == '':
		pagename = 'NoName'
	in_df.to_excel(filename, index=False, sheet_name=pagename)
	print(f'{filename.split("/")[-1]} page {pagename} == {len(in_df)} lines; it`s completed!')

'''
1. get list of wrong-numbers	>>> list_wr_numb
2. get df of source				>>> df_source
3. select part of df_source for deveui in list_wr_numb >>> df_4_fill
4. split df_4_fill for some chanks >>> <xxx>_df_4_fill.xlsx
5. write all files for type <xxx>_df_4_fill.xlsx
'''

# - 1 -
list_wr_numb = f_read_csv(WRONG_NAME)
print(len(list_wr_numb))
print(type(list_wr_numb))

# - 2 -
df_source = f_read_xlsx(SOURCE_NAME)
print(len(df_source))
print(type(df_source))

# - 3 -
df_new_fill = df_source[df_source['DevEUI'].isin(list_wr_numb)]
print(len(df_new_fill))
print(type(df_new_fill))

# - 4 -


# - 5 -
f_write_xlsx(df_new_fill, OUT_NAME)
sys.exit()
