#!/usr/bin/env python3

import typing

import etl_platform


class DBase(object):
    def __init__(self):
        self._setting = etl_platform.set_dbase()
