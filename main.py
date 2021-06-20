#!/usr/bin/env python3.6


import os
from modules import *


# ============== MAIN ===============

def main():
	logging.info('Main-Module is started!')

	# 1--
	# Сохранить Файл-источник, как Файл-добавлений -- it`s released in ConstVar-Module
	# Поменять местами, удалить не нужные и переименовать столбцы
	df_4_fill = read_xlsx(file_source)
	#logging.info(df_4_fill.columns)
	df_4_fill = columns_repair(df_4_fill)
	if not isinstance(df_4_fill, pd.DataFrame):
		print(f'It`s not a class pandas.core.frame.DataFrame !')
		logging.error(f'Unknow format of columns in source-file!')
		return 1
	#-1---------------------------------------------------------------
	
	# 2--
	# Обработать колонку DevEUI
	list_deveui = df_4_fill['DevEUI'].tolist()
	list_repaired_deveui = repair_dev(list_deveui)
	mask_dev = pd.Series(mask_deveui(list_repaired_deveui))
	df_err_dev = df_4_fill[~mask_dev]

	df_4_fill['DevEUI'] = list_repaired_deveui
	df_4_fill = df_4_fill[mask_dev]
	df_4_fill = re_index(df_4_fill)

	##write_xlsx(df_err_dev, file_err_dev)
	write_page_xlsx(df_err_dev, FILE_ERR_OUT, PAGE_ERR_DEV)
	
	df_doubles, df_4_fill = split_doubles(df_4_fill, 'DevEUI')
	df_4_fill = re_index(df_4_fill)

	#write_xlsx(df_doubles, file_doubles)
	write_page_xlsx(df_doubles, FILE_ERR_OUT, PAGE_ERR_DOUBLES)
	#-2---------------------------------------------------------------

	# 3--
	# Обработать колонку RFID
	list_rfid = df_4_fill['RFID значение метки на опоре'].tolist()
	list_repaired_rfid = repair_rfid(list_rfid)
	
	mask_rf = pd.Series(mask_rfid(list_repaired_rfid))
	df_err_rfid = df_4_fill[~mask_rf]
	df_4_fill['RFID значение метки на опоре'] = list_repaired_rfid
	df_4_fill = df_4_fill[mask_rf]
	df_4_fill = re_index(df_4_fill)
	
	write_page_xlsx(df_err_rfid, FILE_ERR_OUT, PAGE_ERR_RFID)
	#-3---------------------------------------------------------------

	# 4--
	# Обработать колонки Координата
	list_coord_Y = df_4_fill['Координата Y WGS84, широта'].tolist()
	list_coord_X = df_4_fill['Координата Х WGS84, долгота'].tolist()
	
	list_coord_Y_rep, mask_coord_Y = check_coord(list_coord_Y, MINMAX_Y)
	list_coord_X_rep, mask_coord_X = check_coord(list_coord_X, MINMAX_X)
	
	if False in mask_coord_X or False in mask_coord_Y:
		mask_coord = pd.Series(list(map(lambda x, y: x and y, mask_coord_X, mask_coord_Y)))
		logging.info('split by coord_err')
		df_err_coord = df_4_fill[~mask_coord]
		df_4_fill['Координата Y WGS84, широта'] = list_coord_Y_rep
		df_4_fill['Координата Х WGS84, долгота'] = list_coord_X_rep
		df_4_fill = df_4_fill[mask_coord]
		df_4_fill = re_index(df_4_fill)
		write_page_xlsx(df_err_coord, FILE_ERR_OUT, PAGE_ERR_COORD)
	#-4---------------------------------------------------------------
	
	# 5--
	# Обработать колонки Сектор / Организация & N сектора
	list_org = df_4_fill['Сектор / Организация'].tolist()
	list_org_rep, list_n_sect = repair_org(list_org, DICT_ORG_SECT)
	df_4_fill['Сектор / Организация'] = list_org_rep
	df_4_fill['N сектора'] = list_n_sect
	#-5---------------------------------------------------------------
	
	# 6--
	# Отделить существующие в системе номера
	df_err_not_motes, df_err_in_lights, df_4_fill = motes_no_lights(df_4_fill, file_db_lights, file_db_motes)

	write_page_xlsx(df_err_not_motes, FILE_ERR_OUT, PAGE_ERR_NOT_MOT)
	write_page_xlsx(df_err_in_lights, FILE_ERR_OUT, PAGE_ERR_ISIN)
	#-6---------------------------------------------------------------
	
	# 13--
	# Записать финальный файл для заливки номеров
	write_new_xlsx(df_4_fill, FILE_4_FILL)
	#-13---------------------------------------------------------------


	logging.info(f"Logging shutdown\n\n")
	logging.shutdown()
	return 0


if __name__ == '__main__':
	sys.exit(main())
