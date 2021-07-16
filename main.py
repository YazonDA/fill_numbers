#!/usr/bin/env python3.6


import os
from modules import *


# ============== MAIN ===============

def main():
	logging.info('Main-Module is started!')
	
	# 1--
	# Сохранить Файл-источник, как Файл-добавлений - это в конце скрипта
	# Поменять местами, удалить не нужные и переименовать столбцы
	df_4_fill = read_xlsx(file_source)
	if not isinstance(df_4_fill, pd.DataFrame):
		print(f'It`s not a class pandas.core.frame.DataFrame !')
		logging.error(f'Unknow format of columns in source-file!')
		return 1

	# 0--
	# Подготовить колонку DevEUI для дальнейшего
	list_deveui = df_4_fill['QR код контроллера'].tolist()
	list_repaired_deveui = repair_dev(list_deveui)
	mask_dev = pd.Series(mask_deveui(list_repaired_deveui))
	df_datetime = df_4_fill[['QR код контроллера', 'Дата внесения изменения']]
	write_new_xlsx(df_datetime, FILE_DT)
	#-0---------------------------------------------------------------

	df_4_fill = columns_repair(df_4_fill)
	#-1---------------------------------------------------------------
	
	# 2--
	# Обработать колонку DevEUI
	df_err_dev = df_4_fill[~mask_dev]
	
	df_4_fill['DevEUI'] = list_repaired_deveui
	df_4_fill = df_4_fill[mask_dev]
	df_4_fill = re_index(df_4_fill)
	
	write_new_xlsx(df_err_dev, FILE_ERR_OUT, PAGE_ERR_DEV)
	
	df_doubles, df_4_fill = split_doubles(df_4_fill, 'DevEUI')
	df_4_fill = re_index(df_4_fill)

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
	list_org_rep, list_n_sect = repair_org(list_org)
	df_4_fill['Сектор / Организация'] = list_org_rep
	df_4_fill['N сектора'] = list_n_sect
	#-5---------------------------------------------------------------
	
	# 5.1--
	# Обработать колонки "Положение светильника относительно дороги"
	# & "Положение светильника на опоре"
	list_4_check = df_4_fill['Положение светильника относительно дороги'].tolist()
	df_4_fill['Положение светильника относительно дороги'] = repair_pole_road(list_4_check, ROAD_LIST)
	list_4_check = df_4_fill['Положение светильника на опоре'].tolist()
	df_4_fill['Положение светильника на опоре'] = repair_pole_road(list_4_check, POLE_LIST)
	#-5.1-------------------------------------------------------------
	
	# 6--
	# Отделить существующие в системе номера
	df_err_not_motes, df_err_in_lights_true, df_err_in_lights_false, df_4_fill = motes_no_lights(df_4_fill)

	write_page_xlsx(df_err_not_motes, FILE_ERR_OUT, PAGE_ERR_NOT_MOT)
	write_page_xlsx(df_err_in_lights_true, FILE_ERR_OUT, PAGE_ERR_ISIN)
	write_new_xlsx(df_err_in_lights_false, FILE_4_REFILL)
	#-6---------------------------------------------------------------
	
	#>>>>>
	zzz = get_table(df_err_in_lights_false['DevEUI'].tolist())
	zzz = pd.DataFrame(zzz, columns=list(range(14)))
	print(zzz)

	return 0
	
	#<<<<<

	# 12--
	# Отделить "плохие" статусы
	list_deveui = df_4_fill['DevEUI'].tolist()
	list_wrong_stat, list_wrong_stat_self = check_stat(list_deveui)
	write_page_xlsx(pd.DataFrame(list_wrong_stat_self, columns=['deveui', 'status']), FILE_ERR_OUT, 'WrongStat')
	'''	DUPLICATE DATA
	df_err_bug_stat = df_4_fill[~df_4_fill['DevEUI'].isin(list_wrong_stat)]
	write_new_xlsx(df_err_bug_stat, FILE_WR_STAT)
	'''
	df_4_fill = df_4_fill[df_4_fill['DevEUI'].isin(list_wrong_stat)]
	#-13---------------------------------------------------------------

	# 13--
	# Записать финальный файл для заливки номеров
	write_new_xlsx(df_4_fill, FILE_4_FILL)
	#-13---------------------------------------------------------------


	logging.info(f"Logging shutdown\n\n")
	logging.shutdown()
	return 0


if __name__ == '__main__':
	sys.exit(main())
