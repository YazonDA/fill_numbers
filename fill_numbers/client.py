import os
import typing
import pandas as pd
import logging

class Client(object):
    def __init__(self, config: typing.Mapping[str, str]):
        path_main = os.getcwd() + '/'

        self._file_in = path_main + str(config["file_in"])
        self._file_out_good = path_main + str(config["file_out_4_fill"])
        self._file_out_rewrite = path_main + str(config["file_out_4_refill"])
        self._file_out_bad = path_main + str(config["file_out_4_err"])

        self._df = ''

        self._list_source_name = tuple(config['cols_source'].split('|'))
        self._list_order_name = tuple(config['cols_order'].split('|'))
        self._list_adding_name = tuple(config['cols_add'].split('|'))
        self._list_4_fill_name = tuple(config['cols_4_fill'].split('|'))

    def run(self) -> bool:
        # get DataFrame
        self.read_xlsx()

        # change all NaN to ''
        self._df = self._df.fillna('')

        # set only needed columns, rename it and set order
        self.name_and_order()

        return len(self._df) >= 0

    def tmp_print(self) -> bool:
        print(self._df)
        return True

    def read_xlsx(self) -> bool:
        try:
            FILENAME = self._file_in
            array = pd.read_excel(FILENAME, engine='openpyxl')
            logging.info(f'{FILENAME.split("/")[-1]} == {len(array)} lines; it`s completed!')
            self._df = array
            return True
        except (FileNotFoundError, IsADirectoryError):
            logging.error(f'FileNotFoundError, IsADirectoryError')
            exit(1)

    def name_and_order(self) -> bool:
        logging.info(f'Module is started!\n')
        
        COLS_SOURCE = self._list_source_name
        ORDER_LIST = self._list_order_name
        ADD_LIST = self._list_adding_name
        NAME_LIST = self._list_4_fill_name
        
        in_df = self._df

        # check format/names in dataframe
        if tuple(in_df.columns) == NAME_LIST:
            return in_df # coz not need 'repaire'

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