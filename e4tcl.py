# -*- coding: utf-8 -*-

import os
import sys
import logging
import argparse

import log
import clparser

logger = logging.getLogger("")


def parse_cl(filepaths):
    logger.debug("%d files will be parsed", len(filepaths))
    output_cl = []
    for cl_path in filepaths:
        output_cl.extend(clparser.load_cl(cl_path))

    return output_cl

def cl2vcard(cl):
    vcard_data = []
    for cl_row in cl:
        vcard_data.append(clparser.create_vcard(cl_row))
    return vcard_data

def write_vcf(dest_path, vcard_data):
    if not os.path.dirname(dest_path):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, 'w', encoding="utf-8") as f:
        for vcard in vcard_data:
            vcard = vcard.replace("\r", "")
            # print("------------")
            # print(repr(vcard))
            # print("------------")
            f.write(vcard)
            # f.write("\n")




if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description="", add_help=False)
    args_parser.add_argument('input', nargs='?', type=str, help='')
    args_parser.add_argument('-d', "--debug", action='store_true', help="debug mode")
    args_parser.add_argument('-o', type=str, help='')
    args = args_parser.parse_args()

    log.setup_logging(enable=args.debug)

    cl = clparser.load_cl(r"d:\_prace\Kontakty.xls")
    vcard_data = cl2vcard(cl)
    write_vcf(r"d:\myVCF.vcf", vcard_data)

