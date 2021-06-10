import pandas as pd
import logging
import string
	

class xlsx():
	pass

def read_xlsx(filename):
	# special for XLSX
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

def check_rus(deveui, const_en='AABBCCEE', const_ru='аАвВсСеЕ'):
	try:
		for tmp_rus in const_ru:
			if tmp_rus in deveui:
				return ''.join(const_en[const_ru.index(chr)] if (chr in const_ru) else chr for chr in deveui)
		return deveui
	except (TypeError):
		logging.error(f'TypeError: argument of type "float" is not iterable')
		return 'ffffffff'

def check_seq(deveui, const_seq=['x005f', 'x000D']):
	try:
		for seq in const_seq:
			while seq in deveui:
				deveui = deveui[:deveui.index(seq)] + deveui[deveui.index(seq) + len(seq):]
		return deveui
	except (TypeError):
		logging.error(f'TypeError: argument of type "float" is not iterable')
		return 'ffffffff'

def check_hex(deveui, const_hex=string.hexdigits):
	try:
		return ''.join(i for i in deveui if i in const_hex)
	except (TypeError):
		logging.error(f'TypeError: argument of type "float" is not iterable')
		return 'ffffffff'

def check_bigQR(deveui, anch=['NwkSEncKey', 'SNwkSIntKey']):
	try:
		if anch[0] in deveui and anch[1] in deveui:
			return deveui[8:25]
		return deveui 
	except (TypeError):
		logging.error(f'TypeError: argument of type "float" is not iterable')
		return 'ffffffff'

def repair_cells(deveui_list):
	answer = []
	for deveui in deveui_list:
		zzz = check_bigQR(deveui)
		zzz = check_seq(zzz)
		zzz = check_rus(zzz)
		zzz = check_hex(zzz)
		logging.info(f'{deveui} ==> {zzz}')
		answer.append(zzz)
	return answer



if __name__ == '__main__':
	print(f'You are make attempt to run this module.\n\
		But it`s only libraries. Not for run!')
	#sys.exit(print('OK!'))