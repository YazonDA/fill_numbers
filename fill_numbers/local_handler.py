import typing
import pandas as pd


class Local(object):
    def __init__(self, config: typing.Mapping[str, str]):
        self._index_4_rep = tuple(map(int, config['index_4_rep'].split(',')))
        self._index_4_calc = tuple(map(int, config['index_4_calc'].split(',')))

    def doit(self, _client) -> pd.DataFrame:
        print(self._index_4_rep)
        TUPLE_4_REPAIR = tuple(_client._list_4_fill_name[i] for i in self._index_4_rep)
        print(TUPLE_4_REPAIR)
        print(_client._df)
        return _client._df