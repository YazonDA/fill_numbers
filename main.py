#!/usr/bin/env python3

import sys
import logging
import configparser
import os

# ============== SET CONSTANTs & VARIABLES ===============

path_main = os.getcwd() + '/'

path_set = path_main + 'setup/settings.ini'
parser = configparser.ConfigParser()
parser.read(path_set)

path_log = path_main + parser["PATH"]["logs"]
path_modul = path_main + parser["PATH"]["modules"]
path_file = path_main + parser["PATH"]["files"]

# ============== SET LOGGER ===============

'''
line_format = "[%(asctime)s] %(levelname)s: %(message)s"
logging.basicConfig(filename=log_file,
						format=line_format,
						level=logging.INFO)
'''
# ============== some MODULES DEFINITION ===============

# ============== MAIN ===============

def main():
	'''
	logging.info(f'\nMAIN was start is successful')
		
	logging.shutdown()
	return 0
	'''

print(__name__)	

if __name__ == '__main__':
	sys.exit(main())

