import configparser
import typing
import logging
import sys

import fill_numbers


class Service(object):
    def __init__(self, config: str):
        parser = configparser.ConfigParser()
        parser.read(config)

        self._client = fill_numbers.Client(parser["client"])
        self._local = fill_numbers.Local(parser["local_handler"])
        self._dbase = fill_numbers.DBase(parser["dbase_handler"])

    def run(self) -> bool:
        logging.info("Starting fill_numbers service...")

        try:
            self._client.run()
        except Exception:
            info = sys.exc_info()
            logging.error("{}: {}".format(info[0].__name__, str(info[1])))
            logging.error("Run Client failed!")
            return False

        self._client._df = self._local.doit(self._client)
        print(self._client._df)
        return True
