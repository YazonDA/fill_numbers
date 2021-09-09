#!/usr/bin/env python3

import typing

import etl_platform


class Local(object):
    def __init__(self):
        self._setting = etl_platform.set_local()
        self._tuple_4_repair = ''

    def run(self, _client) -> bool:
        NAME_LIST = tuple(_client._setting['columns']['cols_4_fill'].split('|'))
        NAME_IND = self._setting['repair']['index_4_rep']

        self._tuple_4_repair = tuple(NAME_LIST[i] for i in NAME_IND)
        return True
