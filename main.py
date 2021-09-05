#!/usr/bin/env python3

import sys
import logging
import typing

import fill_numbers


def main(argv: typing.Sequence[str]) -> int:

    line_format = "[%(asctime)s] %(levelname)s [%(module)s.%(funcName)s: %(lineno)d] %(message)s"
    logging.basicConfig(filename="fill_numbers.log",
                        format=line_format,
                        level=logging.INFO)
    logging.info(f">>>>>>>>>>>>>>>>>>>>>>>>>\
                \nStarting Fill_Numbers logging...\
                \n>>>>>>>>>>>>>>>>>>>>>>>>>")

    service = fill_numbers.Service("fill_numbers.ini")
    answer = service.run()

    logging.shutdown()

    return 0 if answer else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
