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
import re
import logging

import vobject

logger = logging.getLogger("")


def load_cl(cl_path):
    if not os.path.isfile(cl_path):
        raise ValueError("Given cl_path does not exist!")

    with open(cl_path, 'r', encoding="utf-8") as f:
        cl_data = f.readlines()

    # check given file syntax, it has to be table
    if not cl_data or not cl_data[0].strip() != "<table>" or cl_data[-1].strip() != "</table>":
        raise ValueError("Wrong input data format!")

    markups_re = re.compile("<\S+/?>")      # to remove remaining html markups
    parsed_cl = []
    for cl_row in cl_data:
        cl_row = cl_row.strip()
        if cl_row.startswith("<tr>"):
            row_data = [markups_re.sub("", item) for item in cl_row.split("</td>")[:-1]]
            if row_data:
                parsed_cl.append(row_data)
                # lastname, firstname, landline, mobile, email, deperatment, position, place, edited = row_data
            else:
                logger.debug("Line '%s' cl_row skipped because not matching pattern", cl_row)

    logger.debug("%d items parsed from '%s' file", len(parsed_cl), cl_path)

    return parsed_cl


def valid_data(data_str):
    return data_str and "&nbsp;" not in data_str


def create_vcard(cl_row):
    lastname, firstname, landline, mobile, email, department, position, place, edited = cl_row

    if not valid_data(firstname) and not valid_data(lastname):
        logger.debug("Faulty record in contact list, at least one name has to be filled. "
                     "Given firstname: %s, lastname: %s", firstname, lastname)
        return ""

    vcard = vobject.vCard()
    vcard.add("n")
    vcard.n.value = vobject.vcard.Name(family=lastname, given=firstname )
    vcard.add("fn")
    vcard.fn.value = firstname + " " + lastname

    if valid_data(email):
        vcard.add("email")
        vcard.email.type_param = 'work'
        vcard.email.value = email
    # if valid_data(landline):
    #     vcard.add("tel")
    #     vcard.tel.value = landline
    #     vcard.tel.type_param = 'work,voice'
    #     print(landline, repr(landline))
    if valid_data(mobile):
        vcard.add("tel")
        vcard.tel.value = mobile
        vcard.tel.type_param = 'cell,voice'
    if valid_data(position):
        vcard.add("role")
        vcard.role.value = position
    if valid_data(department):
        vcard.add("title")
        vcard.title.value = department
    if valid_data(place):
        vcard.add("adr")
        vcard.adr.value = vobject.vcard.Address(city=place)
        vcard.adr.type_param = 'work'
    if valid_data(edited):
        vcard.add("note")
        vcard.note.value = "Updated on %s" % edited

    vcard.prettyPrint()

    return vcard.serialize()


