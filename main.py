#!/usr/bin/env python3

import sys
import logging
import typing

import etl_platform


def main(argv: typing.Sequence[str]) -> int:

    line_format = "[%(asctime)s] %(levelname)s [%(module)s.%(funcName)s: %(lineno)d] %(message)s"
    logging.basicConfig(filename="etl_platform.log",
                        format=line_format,
                        level=logging.INFO)
    logging.info(f"\n\nStarting Etl Platform logging...\
                \n>>>>>>>>>>>>>>>>>>>>>>>>>")

    if len(argv) > 1:
        SOURCE_FILE = argv[1]
    elif len(argv) == 1:
        SOURCE_FILE = 'Non file'
    else:
        logging.error('Something wrong & unreal')
        return 1

    service = etl_platform.Service(SOURCE_FILE)
    answer = service.run()

    logging.info(f"\n<<<<<<<<<<<<<<<<<<<<<<<<<\
                \nClosing Etl Platform logging...\n\n\n")
    logging.shutdown()

    return 0 if answer else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
