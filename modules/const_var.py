import os
import configparser
import string
import re


# ============== SET CONSTANTs & VARIABLES ===============

# Names of some Paths
path_main = os.getcwd() + '/'

path_set = path_main + 'setup/settings.ini'
parser = configparser.ConfigParser()
parser.read(path_set)

path_log = path_main + parser["PATH"]["logs"]
path_modul = path_main + parser["PATH"]["modules"]
path_file = path_main + parser["PATH"]["files"]

# Names of some Files
FILE_LOGGER = path_log + 'tmp_log'
file_source = path_file + parser['FILES']['f_source']
file_4_fill = path_file + parser['FILES']['f_4_fill']
file_4_pass = path_file + parser['FILES']['f_4_pass']
file_err_dev = path_file + parser['FILES']['f_err_dev']
file_err_rfid = path_file + parser['FILES']['f_err_rfid']
file_err_coord = path_file + parser['FILES']['f_err_coord']
file_doubles = path_file + parser['FILES']['f_doubles']
file_org = path_file + parser['FILES']['f_org']
file_err_not_motes = path_file + parser['FILES']['f_err_not_motes']
file_isin = path_file + parser['FILES']['f_err_isin']
#file_db_motes = path_file + 'tst_motes.result'
#file_db_lights = path_file + 'tst_lights.result'

# List of some  Column`s Names
cols_source = parser['LISTS']['cols_source'].split('|')
cols_order = parser['LISTS']['cols_order'].split('|')
cols_add = parser['LISTS']['cols_add'].split('|')
cols_4_fill = parser['LISTS']['cols_4_fill'].split('|')
dict_cols_caption = {'cols_source': cols_source, 'cols_order': cols_order, 'cols_add': cols_add, 'cols_4_fill': cols_4_fill}
dict_org_sect = dict(zip(parser['LISTS']['org_list'].split('|'), parser['LISTS']['sect_list'].split('|')))

# sample for some compare
const_ru = 'аАвВсСеЕ'
const_en = 'AABBCCEE'
const_seq = ['x005f', 'x000D']
const_deveui = string.hexdigits
const_rfid = string.ascii_letters + string.digits
format_deveui = r'0016[cC]00000[0-9a-fA-F]{6}'
minmax_Y = list(map(float, parser['COORD']['minmax_Y'].split('|')))
minmax_X = list(map(float, parser['COORD']['minmax_X'].split('|')))

# ============== SET LOGGER ===============
LOGGER_FORMAT = "[%(asctime)s] %(levelname)s [%(funcName)s: %(lineno)d] %(message)s"
