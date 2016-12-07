#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
import sql_parse
import make_mixin
import make_crud


TEMPALTE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "templates")


def metat(sql_filename, project_path, schema, table_name, action):
    sql = open(sql_filename, "r").read()
    fields = sql_parse.create_table_parse(sql, schema, table_name)

    if fields:
        if action == "mixin":
            make_mixin.make_mixin(
                TEMPALTE_PATH, project_path, schema, table_name, fields)

        elif action == "crud":
            handlers_folder = sys.argv[5] \
                if len(sys.argv) > 5 else "handlers"

            make_crud.make_crud(
                TEMPALTE_PATH, project_path, schema, table_name, fields,
                handlers_folder)

    else:
        print "Sorry(!"


if __name__ == '__main__':
    if len(sys.argv) > 1:
        sql_filename = sys.argv[1]
        project_path = sys.argv[2]
        schema, table_name = sys.argv[3].split(".")
        action = sys.argv[4]

        metat(sql_filename, project_path, schema, table_name, action)

    else:
        print "sql_filename, project_path, schema.table_name, action"
