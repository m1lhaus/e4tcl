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
    logger.info("Saving contacts to '%s'", dest_path)
    print("Saving contacts to '%s'" % dest_path)

    with open(dest_path, 'w', encoding="utf-8") as f:
        for vcard in vcard_data:
            f.write(vcard)
            f.write("\n")


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description="", add_help=False)
    args_parser.add_argument('input', nargs='*', type=str, help='')
    args_parser.add_argument('-d', "--debug", action='store_true', help="debug mode")
    args_parser.add_argument('-o', '--output', type=str, help='')
    args = args_parser.parse_args()

    # turn ON/OFF logging
    log.setup_logging(enable=args.debug)

    # setup output directory
    if args.output:
        out_dir = os.path.dirname(args.output)
        if not os.path.isdir(out_dir):
            logger.info("Creating output directory '%s'", out_dir)
            os.makedirs(out_dir)
    else:
        args.output = os.path.join(os.getcwd(), "contacts.vcf")

    cl_merged = []
    for cl_path in args.input:
        if not os.path.isfile(cl_path):
            raise AttributeError("Given cl_path does not exist!")

        cl_merged.extend(clparser.load_cl(cl_path))
    vcard_data = cl2vcard(cl_merged)

    if vcard_data:
        write_vcf(args.output, vcard_data)
    else:
        logger.warning("No contacts found/given!")
        print("No contacts found/given!")

