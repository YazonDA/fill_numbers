#!/usr/bin/env python3

import sys
import logging
import logging.config
import configparser
import os

from modules import *

# ============== SET CONSTANTs & VARIABLES ===============

path_main = os.getcwd() + '/'

path_set = path_main + 'setup/settings.ini'
parser = configparser.ConfigParser()
parser.read(path_set)

path_log = path_main + parser["PATH"]["logs"]
path_modul = path_main + parser["PATH"]["modules"]
path_file = path_main + parser["PATH"]["files"]

file_log = path_log + 'tmp_log'

# ============== SET LOGGER ===============

 
logging.config.fileConfig('setup/logging.conf')
logger = logging.getLogger("mainApp")

logger.info("Program started")

'''
line_format = "[%(asctime)s] [%(name)s] %(levelname)s: %(message)s"
logging.basicConfig(filename=file_log,
						format=line_format,
						level=logging.INFO)
'''
# ============== MAIN ===============

def main():
	logger.info("Main started!")

	tmp_name = '/home/yda/Documents/check_fill_2_platform/tst_add_1_full_double_03.xlsx'
	logger.info(r_w_xlsx.read_xlsx(tmp_name))
	r_w_xlsx.ppprint()

	logger.info("Main Done!")

	logging.shutdown()
	return 0

	'''
	logging.info(f'\nMAIN was start is successful')
		
	'''
	#logging.info(xlsx.read_xlsx(tmp_name))


if __name__ == '__main__':
	sys.exit(main())

