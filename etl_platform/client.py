#!/usr/bin/env python3

import os
import typing
import pandas as pd
import logging

import etl_platform
#.settings as Settings
#import etl_platform


class Client(object):
    def __init__(self):

        self._setting = etl_platform.set_client()
        self._local = etl_platform.Local()
        self._dbase = etl_platform.DBase()

        self._df = ''

    def run(self) -> bool:
        # get DataFrame
        self.read_xlsx()

        # change all NaN to ''
        self._df = self._df.fillna('')

        # set only needed columns, rename it and set order
        self.name_and_order()

        return len(self._df) >= 0

    def do_it(self) -> bool:
        self._local.run(self)
        return True

    def tmp_print(self) -> bool:
        print(self._df)
        return True


    def read_xlsx(self) -> bool:
        try:
            path_main = os.getcwd() + '/'
            files = self._setting['file_name']
            
            FILENAME = path_main + files['source']
            array = pd.read_excel(FILENAME, engine='openpyxl')
            
            logging.info(f'{FILENAME.split("/")[-1]} == {len(array)} lines; it`s completed!')
            self._df = array
            return True
        
        except (FileNotFoundError, IsADirectoryError):
            logging.error(f'FileNotFoundError, IsADirectoryError')
            exit(1)

    def name_and_order(self) -> bool:
        logging.info(f'Module is started!')
        
        columns_ini = self._setting['columns']

        COLS_SOURCE = tuple(columns_ini['cols_source'].split('|'))
        ORDER_LIST = tuple(columns_ini['cols_order'].split('|'))
        ADD_LIST = tuple(columns_ini['cols_add'].split('|'))
        NAME_LIST = tuple(columns_ini['cols_4_fill'].split('|'))

        in_df = self._df

        # check format/names in dataframe
        if tuple(in_df.columns) == NAME_LIST:
            return True # coz not need 'repaire'

        elif tuple(in_df.columns) == COLS_SOURCE:
            # columns_add
            for col_name in ADD_LIST:
                in_df[col_name] = 0

            # columns_order
            in_df = in_df.reindex(columns=ORDER_LIST)
            # columns_rename
            in_df.columns = NAME_LIST

            logging.info(f'Module will return this DF:\n{len(in_df)} rows; {type(in_df)}')
            if not isinstance(in_df, pd.DataFrame):
                logging.error(f'Unknow format of columns in source-file!')
                exit(1)
            self._df = in_df
            return True
        return False