import pandas as pd
import logging
import string
import re
import csv



def read_xlsx(filename):
	# special for XLSX
	array = []
	try:
		array = pd.read_excel(filename)
		logging.info(f'{filename.split("/")[-1]} == {len(array)} lines; it`s completed!')
		return array
	except (FileNotFoundError, IsADirectoryError):
		logging.error(f'FileNotFoundError, IsADirectoryError')
		exit(1)

def write_xlsx(in_df, filename):
	# special for XLSX
	in_df.to_excel(filename, index=False)
	logging.info(f'{filename.split("/")[-1]} == {len(in_df)} lines; it`s completed!')

def write_csv(arr, filename):
	with open(filename, 'w') as csv_file:
		writer = csv.writer(csv_file, dialect = 'excel')
		for i in arr:
			writer.writerow([i])
	logging.info(f'{filename.split("/")[-1]} == {len(arr)} lines; it`s completed!')
	return True

def columns_add(in_df, add_list):
	for col_name in add_list:
		in_df[col_name] = 0
	logging.info('it`s completed!')
	return in_df

def columns_order(in_df, order_list):
	in_df = in_df.reindex(columns=order_list)
	logging.info('it`s completed!')
	return in_df

def columns_rename(in_df, name_list):
	in_df.columns = name_list
	#cols = list(tmp_df.columns.values)
	logging.info('it`s completed!')
	return in_df
'''
def columns_list(in_df):
	return list(in_df.columns.values)
'''
def check_rus(deveui, const_en='AABBCCEE', const_ru='аАвВсСеЕ'):
	try:
		for tmp_rus in const_ru:
			if tmp_rus in deveui:
				return ''.join(const_en[const_ru.index(chr)] if (chr in const_ru) else chr for chr in deveui)
		return deveui
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "ffffffff"')
		return 'ffffffff'

def check_seq(deveui, const_seq=['x005f', 'x000D']):
	try:
		for seq in const_seq:
			while seq in deveui:
				deveui = deveui[:deveui.index(seq)] + deveui[deveui.index(seq) + len(seq):]
		return deveui
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "ffffffff"')
		return 'ffffffff'

def check_hex(deveui, const_deveui=string.hexdigits):
	try:
		zzz = ''.join(i for i in deveui if i in const_deveui)
		if len(zzz) == 0:
			return 'ffffffff'
		return zzz
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "ffffffff"')
		return 'ffffffff'

def check_dec(rfid, const_rfid=string.ascii_letters+string.digits):
	try:
		zzz = ''.join(i for i in rfid if i in const_rfid)
		if len(zzz) == 0:
			return 'ffffffff'
		return zzz
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "ffffffff"')
		return 'ffffffff'

def check_bigQR(deveui, anch=['NwkSEncKey', 'SNwkSIntKey']):
	try:
		if anch[0] in deveui and anch[1] in deveui:
			return deveui[8:25]
		return deveui 
	except (TypeError):
		#logging.error(f'TypeError: argument of type "float" is not iterable. Returned "ffffffff"')
		return 'ffffffff'

def repair_dev(deveui_list):
	answer = []
	for deveui in deveui_list:
		deveui = check_bigQR(deveui)
		deveui = check_seq(deveui)
		deveui = check_rus(deveui)
		deveui = check_hex(deveui)
		answer.append(deveui.lower())
	logging.info('it`s completed!')
	return answer

def mask_deveui(deveui_list, pattern_deveui=r'0016[cC]00000[0-9a-fA-F]{6}'):
	mask = []
	for deveui in deveui_list:
		mask.append(bool(re.fullmatch(pattern_deveui, deveui)))
	logging.info('it`s completed!')
	return mask

def mask_double(deveui_list):
	mask = []
	for ind, deveui in enumerate(deveui_list):
		mask.append(bool(deveui_list.count(deveui) == 1))
		if not bool(ind%5000):
			logging.info(f'{ind} lines processed.')
	logging.info('it`s completed!')
	return mask

def repair_rfid(rfid_list):
	answer = []
	for rfid in rfid_list:
		zzz = check_seq(rfid)
		zzz = check_dec(zzz)
		answer.append(zzz)
	logging.info('it`s completed!')
	return answer

def mask_rfid(rfid_list):
	mask = []
	for rfid in rfid_list:
		mask.append(bool(len(rfid) >= 6))
	logging.info('it`s completed!')
	return mask

def check_coord(coord_list, minmax):
	mask = []
	for ind, coord in enumerate(coord_list):
		if isinstance(coord, str):
			if re.match(r'^\d{2},\d{4,}$', coord):
				coord_list[ind] = float(coord.replace(',', '.'))
				coord = coord_list[ind]
		if isinstance(coord, float):
			mask.append(bool(minmax[0] <= coord <= minmax[1]))
			continue
		mask.append(False)
	logging.info('it`s completed!')
	return coord_list, mask

def repair_org(org_list, dict_org_sect):
	n_sect_list = []
	for ind in range(len(org_list)):
		if org_list[ind] not in dict_org_sect:
			org_list[ind] = 'Неопределен.'
		n_sect_list.append(dict_org_sect[org_list[ind]])
		if not bool(ind%5000):
			logging.info(f'{ind} lines processed.')
	logging.info('it`s completed!')
	return (org_list, n_sect_list)


if __name__ == '__main__':
	print(f'You are make attempt to run this module.\n\
		But it`s only libraries. Not for run!')
	#sys.exit(print('OK!'))