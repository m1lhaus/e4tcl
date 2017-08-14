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


"""
Helper tools for parsing contact lists from XLS format and create vCard contacts
-   parse XLS cl list
-   fill vCard
-   dump vCard contacts to VCF file
"""

import os
import sys
import re
import logging

logger = logging.getLogger("")


def load_cl(cl_path: str) -> list:
    logger.debug("Reading file '%s'", cl_path)
    with open(cl_path, 'r', encoding="utf-8") as f:
        cl_data = f.readlines()

    # check given file syntax, it has to be table
    if not cl_data or not cl_data[0].strip() != "<table>" or cl_data[-1].strip() != "</table>":
        raise ValueError("Wrong input data format!")

    markups_re = re.compile("<\S+/?>")  # to remove remaining html markups
    parsed_cl = []
    for cl_row in cl_data:
        cl_row = cl_row.strip()
        if cl_row.startswith("<tr>"):
            row_data = [markups_re.sub("", item) for item in cl_row.split("</td>")[:-1]]
            if row_data:
                parsed_cl.append(row_data)
            else:
                logger.debug("Line '%s' cl_row skipped because not matching pattern", cl_row)

    logger.debug("%d items parsed from '%s' file", len(parsed_cl), cl_path)
    return parsed_cl


def valid_data(data_str: str) -> bool:
    return data_str and "&nbsp;" not in data_str


def nokia_utf8_normalize(string: str) -> str:
    byte_string = string.encode("utf-8")
    norm_string = []
    for byte in byte_string:
        if int(byte) > 127:
            byte = "=%02X" % byte       # nokia format for non-ascii chars
        else:
            byte = chr(byte)
        norm_string.append(str(byte))
    norm_string = "".join(norm_string)
    norm_string = norm_string.replace(" ", "=20")       # just in case we have some white space in name
    return norm_string


def create_vcard(cl_row: tuple, nokia: bool) -> str:
    lastname, firstname, landline, mobile, email, department, position, place, edited = cl_row
    logger.debug("Parsing contact: %s", cl_row)

    if not valid_data(firstname) and not valid_data(lastname):
        logger.info("Faulty record in contact list, at least one name has to be filled. "
                    "Given firstname: %s, lastname: %s", firstname, lastname)
        return ""

    vcard_data = []

    # generic vcard
    if not nokia:
        vcard_data.append("BEGIN:VCARD")
        vcard_data.append("VERSION:3.0")
        vcard_data.append("N:%s;%s;;;" % (lastname, firstname))
        vcard_data.append("FN:%s %s" % (firstname, lastname))
        if valid_data(email):
            vcard_data.append("EMAIL;TYPE=work:%s" % email)
        if valid_data(mobile):
            vcard_data.append("TEL;TYPE=cell:%s" % mobile)
        if valid_data(landline):
            vcard_data.append("TEL;TYPE=work:%s" % landline)
        if valid_data(position):
            vcard_data.append("ROLE:%s" % position)
        if valid_data(department):
            vcard_data.append("TITLE:%s" % department)
        if valid_data(place):
            vcard_data.append("ADR;TYPE=work:;;;%s;;;" % place)
        if valid_data(edited):
            vcard_data.append("NOTE:Updated on %s" % edited)
        vcard_data.append("END:VCARD")

    # vcard in nokia format
    else:
        split_contact = valid_data(landline)        # nokia can't handle vcard with two phone numbers

        vcard_data.append("BEGIN:VCARD")
        vcard_data.append("VERSION:2.1")
        vcard_data.append("N;ENCODING=QUOTED-PRINTABLE;CHARSET=UTF-8:;=")
        # adjust maximum name length
        max_len = 14 if split_contact else 16               # if contact is split, we need two chars for M or W flag
        name_len = len(firstname) + len(lastname) + 1       # 1 is for space
        if name_len > max_len:
            trim_len = name_len - max_len       # get diff
            if trim_len > len(firstname):       # if trimming firstname is not enough
                trim_len -= len(firstname)
                firstname = ""
                lastname = lastname[:-trim_len]
            else:
                firstname = firstname[:-trim_len]
        name_appendix = " M" if split_contact else ""       # flag to distinguish two contacts with same name
        vcard_data.append("%s=20%s;;;" % (nokia_utf8_normalize(lastname),
                                          nokia_utf8_normalize(firstname + name_appendix)))     # lastname first
        if valid_data(mobile):
            vcard_data.append("TEL;TYPE=cell:%s" % mobile)
        if valid_data(email):
            vcard_data.append("EMAIL;TYPE=work:%s" % email)
        vcard_data.append("END:VCARD")

        # second contact with landline phone number
        if split_contact:
            vcard_data.append("BEGIN:VCARD")
            vcard_data.append("VERSION:2.1")
            vcard_data.append("N;ENCODING=QUOTED-PRINTABLE;CHARSET=UTF-8:;=")
            name_appendix = " P"
            vcard_data.append("%s=20%s;;;" % (nokia_utf8_normalize(lastname),
                                              nokia_utf8_normalize(firstname + name_appendix)))
            vcard_data.append("TEL;TYPE=cell:%s" % landline)
            if valid_data(email):
                vcard_data.append("EMAIL;TYPE=work:%s" % email)
            vcard_data.append("END:VCARD")

    return "\n".join(vcard_data)


def cl2vcard(cl, nokia):
    vcard_data = []
    for cl_row in cl:
        vcard_data.append(create_vcard(cl_row, nokia))
    return vcard_data


def write_vcf(dest_path, vcard_data):
    logger.info("Saving contacts to '%s'", dest_path)

    with open(dest_path, 'w', encoding="utf-8") as f:
        for vcard in vcard_data:
            f.write(vcard)
            f.write("\n")
