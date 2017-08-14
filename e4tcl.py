# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Milan Herbig <milanherbig[at]gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
import sys
import logging
import argparse

import log
import cltools

import maindialog

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


logger = logging.getLogger("")


# def parse_cl(filepaths):
#     logger.debug("%d files will be parsed", len(filepaths))
#     output_cl = []
#     for cl_path in filepaths:
#         output_cl.extend(clparser.load_cl(cl_path))
#
#     return output_cl


# def cl2vcard(cl):
#     vcard_data = []
#     for cl_row in cl:
#         vcard_data.append(clparser.create_vcard(cl_row))
#     return vcard_data
#
#
# def write_vcf(dest_path, vcard_data):
#     logger.info("Saving contacts to '%s'", dest_path)
#     print("Saving contacts to '%s'" % dest_path)
#
#     with open(dest_path, 'w', encoding="utf-8") as f:
#         for vcard in vcard_data:
#             f.write(vcard)
#             f.write("\n")


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description="", add_help=True)
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

            cl_merged.extend(cltools.load_cl(cl_path))
        vcard_data = cltools.cl2vcard(cl_merged, args.nokia)

        if vcard_data:
            cltools.write_vcf(args.output, vcard_data)
            print("Contacts saved to '%s'" % args.output)
        else:
            logger.warning("No contacts found/given!")
            print("No contacts found/given!")
    else:
        app = QApplication(sys.argv)
        app.setOrganizationName("e4tcl")
        app.setOrganizationDomain("com.e4tcl.e4tcl")
        app.setApplicationName("e4tcl")
        dialog = maindialog.MainDialog(args)
        dialog.show()
        app.exec_()
