import configparser
import typing
import logging
import sys

import cl4f


class Service(object):
    def __init__(self, config: str):
        parser = configparser.ConfigParser()
        parser.read(config)

        self._client = cl4f.Client(parser["client"])
        self._local = cl4f.Local(parser["local_handler"])
        self._dbase = cl4f.DBase(parser["dbase_handler"])

    def run(self) -> bool:
        logging.info("Starting cl4f service...")

        try:
            self._client.run()
        except Exception:
            info = sys.exc_info()
            logging.error("{}: {}".format(info[0].__name__, str(info[1])))
            logging.error("Run Client failed!")
            return False

        print(self._client._df)
        return True
