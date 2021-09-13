#!/usr/bin/env python3

import typing
import logging
import sys

import etl_platform


class Service(object):
    def __init__(self, source):
        self._client = etl_platform.Client(source)

    def run(self) -> bool:
        logging.info("Starting etl_platform service...")

        try:
            self._client.run()
        except Exception:
            info = sys.exc_info()
            logging.error("{}: {}".format(info[0].__name__, str(info[1])))
            logging.error("Run Client failed!")
            return False

        self._client.tmp_print()
        self._client.do_it()
        return True
