#-*- coding: utf-8 -*-

import os
from jinja2 import Environment
from jinja2 import FileSystemLoader


def make_mixin(template_path, path, schema, table_name, fields):
    mixins_path = os.path.join(path, "mixins")

    if not os.path.exists(mixins_path):
        os.mkdir(mixins_path)
        open(os.path.join(mixins_path, "__init__.py"), "w").close()

    filepath = os.path.join(mixins_path, "{}_mixin.py".format(table_name))

    if not os.path.isfile(filepath):
        loader = FileSystemLoader(template_path)
        env = Environment(loader=loader)
        template = env.get_template("mixins/mixin.tpl")
        
        context = {
            "schema": schema,
            "table_name": table_name,
            "class_name": "".join([l.title() for l in table_name.split("_")]),
            "table_name_upper": table_name.upper(),
            "fields": fields,
            "fields_last_index": len(fields) - 1,
        }

        template.stream(context).dump(open(filepath, "w"))
