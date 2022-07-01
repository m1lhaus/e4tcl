# -*- coding: utf-8 -*-

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

import openpyxl
import pandas as pd

logger = logging.getLogger("")


def load_cl(cl_path: str) -> list:
    logger.debug("Reading file '%s'", cl_path)
    wb = openpyxl.load_workbook(filename=cl_path, read_only=True, data_only=True)
    ws = wb.active
    df = pd.DataFrame(ws.values)
    df.columns = df.iloc[0]
    df = df.drop(0)
    df.index = range(df.shape[0])
    return df


def nokia_utf8_normalize(string: str) -> str:
    byte_string = string.encode("utf-8")
    norm_string = []
    for byte in byte_string:
        if int(byte) > 127:
            byte = "=%02X" % byte  # nokia format for non-ascii chars
        else:
            byte = chr(byte)
        norm_string.append(str(byte))
    norm_string = "".join(norm_string)
    norm_string = norm_string.replace(" ", "=20")  # just in case we have some white space in name
    return norm_string


def create_vcard(cl_row: pd.Series, nokia: bool) -> str:
    logger.debug("Parsing contact: %s", cl_row)

    lastname = cl_row["Příjmení | Název"]
    firstname = cl_row["Jméno"]
    name_shortcut = cl_row["Zkratka zaměstnance"]
    mobile = cl_row["Číslo mobilního telefonu"]
    email = cl_row["E-mail"]
    department = cl_row["Organizační jednotka"]
    position = cl_row["Název pozice"]
    city = cl_row["Pracoviště"]
    building = cl_row["Budova"]
    floor = cl_row["Patro"]
    office = cl_row["Číslo kanceláře"]

    vcard_data = []

    # generic vcard
    if not nokia:
        vcard_data.append("BEGIN:VCARD")
        vcard_data.append("VERSION:3.0")
        vcard_data.append("N:%s;%s;;;" % (lastname, firstname))
        vcard_data.append("FN:%s %s" % (firstname, lastname))
        vcard_data.append("EMAIL;TYPE=work:%s" % email)
        vcard_data.append("NICKNAME:%s" % name_shortcut)
        vcard_data.append("TEL;TYPE=cell:%s" % mobile)
        vcard_data.append("ROLE:%s" % position)
        vcard_data.append("ORG:%s" % department)
        vcard_data.append(f"ADR;TYPE=work:;{building};{floor} - kancelář {office};{city};;;")
        vcard_data.append("END:VCARD")

    # vcard in nokia format
    else:
        vcard_data.append("BEGIN:VCARD")
        vcard_data.append("VERSION:2.1")
        vcard_data.append("N;ENCODING=QUOTED-PRINTABLE;CHARSET=UTF-8:;=")
        # adjust maximum name length
        max_len = 16  # if contact is split, we need two chars for M or W flag
        name_len = len(firstname) + len(lastname) + 1  # 1 is for space
        if name_len > max_len:
            trim_len = name_len - max_len  # get diff
            if trim_len > len(firstname):  # if trimming firstname is not enough
                trim_len -= len(firstname)
                firstname = ""
                lastname = lastname[:-trim_len]
            else:
                firstname = firstname[:-trim_len]
        vcard_data.append("%s=20%s;;;" % (nokia_utf8_normalize(lastname),
                                          nokia_utf8_normalize(firstname)))  # lastname first
        vcard_data.append("TEL;TYPE=cell:%s" % mobile)
        vcard_data.append("EMAIL;TYPE=work:%s" % email)
        vcard_data.append("END:VCARD")

    return "\n".join(vcard_data)


def cl2vcard(cl: pd.DataFrame, nokia: bool) -> list[str]:
    vcard_data = []
    for cl_row in cl.iterrows():
        vcard_data.append(create_vcard(cl_row[1], nokia))
    return vcard_data


def write_vcf(dest_path, vcard_data):
    logger.info("Saving contacts to '%s'", dest_path)

    with open(dest_path, 'w', encoding="utf-8") as f:
        for vcard in vcard_data:
            f.write(vcard)
            f.write("\n")
