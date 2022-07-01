# -*- coding: utf-8 -*-

import os
import sys
import logging
import argparse
from typing import List

import pandas as pd

import log
import cltools

import maindialog

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

logger = logging.getLogger("")

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description="Script takes list of XLSX files with contacts generated from InfoPortal and, merges them and coverts "
                                                      "them to VCard.", add_help=True)
    args_parser.add_argument('input', nargs='*', type=str, help='list of XLS files with contacts')
    args_parser.add_argument('-d', "--debug", action='store_true', help="enables debug logging")
    args_parser.add_argument('-o', '--output', type=str, help='output filepath of VCF file')
    args_parser.add_argument('-n', '--nokia', action='store_true', help="use Nokia compatible VCF format")
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

    if args.input:
        cl_merged = []
        for cl_path in args.input:
            if not os.path.isfile(cl_path):
                raise AttributeError("Given cl_path does not exist!")

            cl_merged.append(cltools.load_cl(cl_path))
        if not cl_merged:
            print("No contacts loaded!")
            sys.exit(1)
        else:
            if len(cl_merged) > 1:
                cl_merged = pd.concat(cl_merged)
                cl_merged = cl_merged.drop_duplicates()
            else:
                cl_merged = cl_merged[0]

        vcard_data = cltools.cl2vcard(cl_merged, args.nokia)

        if vcard_data:
            cltools.write_vcf(args.output, vcard_data)
            print("Contacts saved to '%s'" % args.output)
        else:
            logger.warning("No contacts found/given!")
            print("No contacts found/given!")
    else:
        app = QApplication(sys.argv)
        app.setOrganizationName("dqcl")
        app.setOrganizationDomain("com.dqcl.dqcl")
        app.setApplicationName("dqcl")
        dialog = maindialog.MainDialog(args)
        dialog.show()
        app.exec_()
