import typing
import pandas as pd


class Local(object):
    def __init__(self, config: typing.Mapping[str, str]):
        self._index_4_rep = tuple(map(int, config['index_4_rep'].split(',')))
        self._index_4_calc = tuple(map(int, config['index_4_calc'].split(',')))
        self._tuple_4_repair = ''

    def doit(self, _client) -> pd.DataFrame:
        #print(self._index_4_rep)

        self._tuple_4_repair = tuple(_client._list_4_fill_name[i] for i in self._index_4_rep)
        self.repair_column(_client)

        #print(TUPLE_4_REPAIR)
        #print(_client._df)

        return _client._df

    def repair_column(self, _client):
        IN_DF = _client._df
        TUPLE_4_REPAIR = self._tuple_4_repair

        for _caption in TUPLE_4_REPAIR:
            if _caption == 'DevEUI':
                tuple_deveui = tuple(IN_DF[_caption].tolist())
                answer = []
                for deveui in tuple_deveui:
                    deveui = check_bigQR(deveui, repair_dev_dict)
                    deveui = check_seq(deveui, repair_dev_dict)
                    deveui = check_rus(deveui, repair_dev_dict)
                    deveui = check_hex(deveui, repair_dev_dict)
                    answer.append(deveui.lower())
            elif _caption == '':
                pass
            elif _caption == '':
                pass
            elif _caption == '':
                pass
            elif _caption == '':
                pass
            elif _caption == '':
                pass
            else:
                #error
                pass

        print('from repair_column')
        _client.tmp_print()

def init_repair(repair_dev_dict):
    global ERR_MSG
    ERR_MSG = repair_dev_dict['ERR_MSG']

def check_hex(deveui, columns_name, repair_dict, repair_dev_dict):
    try:
        deveui = ''.join(i for i in deveui if i in repair_dict[columns_name]['format'])
        if len(deveui) == 0:
            return ERR_MSG
        return deveui
    except (TypeError):
        #logging.error(f'TypeError: argument of type "float" is not iterable. Returned "f"')
        return ERR_MSG

def check_digits(rfid, columns_name, repair_dict, repair_dev_dict):
    try:
        rfid = ''.join(i for i in rfid if i in repair_dict[columns_name]['format'])
        if len(rfid) == 0:
            return ERR_MSG
        return rfid
    except (TypeError):
        #logging.error(f'TypeError: argument of type "float" is not iterable. Returned "f"')
        return ERR_MSG

def check_rus(deveui, repair_dev_dict):
    try:
        for tmp_rus in repair_dev_dict['CONST_RU']:
            if tmp_rus in deveui:
                return ''.join(repair_dev_dict['CONST_EN'][repair_dev_dict['CONST_RU'].index(chr)] if (chr in repair_dev_dict['CONST_RU']) else chr for chr in deveui)
        return deveui
    except (TypeError):
        #logging.error(f'TypeError: argument of type "float" is not iterable. Returned "f"')
        return ERR_MSG

def check_seq(deveui, repair_dev_dict):
    try:
        for seq in repair_dev_dict['CONST_SEQ']:
            while seq in deveui:
                deveui = deveui[:deveui.index(seq)] + deveui[deveui.index(seq) + len(seq):]
        return deveui
    except (TypeError):
        #logging.error(f'TypeError: argument of type "float" is not iterable. Returned "f"')
        return ERR_MSG

def check_bigQR(deveui, repair_dev_dict):
    anch=repair_dev_dict['ERR_ANCH_QR']
    try:
        if anch in deveui:
            return (re.match(repair_dev_dict['FORMAT_BIGQR'], deveui)).group(1)
        return deveui 
    except (TypeError):
        #logging.error(f'TypeError: argument of type "float" is not iterable. Returned "f"')
        return ERR_MSG
    except (AttributeError):
        #logging.error(f'AttributeError: dev == {deveui}')
        return ERR_MSG

def split_doubles(in_df, col_name):
    df_doubles = in_df[in_df.duplicated(subset=col_name, keep=False)]
    df_N_doubles = in_df.drop_duplicates(subset=col_name, keep=False)
    logging.info('it`s completed!')
    return df_doubles, df_N_doubles
