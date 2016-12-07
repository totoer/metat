#-*- coding: utf-8 -*-

import re


def create_table_parse(sql, schema, table_name):
    sql = sql.replace("\n", " ")
    sql = re.sub(r" +", " ", sql)

    name = "{}.{}".format(schema, table_name)
    
    r = re.findall(r"create table {} ?\((.+?)\);".format(name), sql, re.I)
    if r:
        fields = r[0].split(",")
        fields = [field.strip().split() for field in fields]
        return [{"name": field[0], "type": field[1]} for field in fields]

    else:
        return None
