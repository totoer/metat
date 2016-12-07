#-*- coding: utf-8 -*-

import os
from jinja2 import Environment
from jinja2 import FileSystemLoader

import make_mixin


def make_init_handler(template, path, schema, table_name, fields):
    filepath = os.path.join(path, "__init__.py")
    
    context = {
        "table_name": table_name,
        "class_name": "".join([l.title() for l in table_name.split("_")]),
        "fields": fields,
    }

    template.stream(context).dump(open(filepath, "w"))


def make_create_handler(template, path, schema, table_name, fields):
    filepath = os.path.join(path, "create_handler.py")
    
    context = {
        "table_name": table_name,
        "class_name": "".join([l.title() for l in table_name.split("_")]),
        "fields": fields,
    }

    template.stream(context).dump(open(filepath, "w"))


def make_update_handler(template, path, schema, table_name, fields):
    filepath = os.path.join(path, "update_handler.py")
    
    context = {
        "table_name": table_name,
        "class_name": "".join([l.title() for l in table_name.split("_")]),
        "fields": fields,
    }

    template.stream(context).dump(open(filepath, "w"))

def make_delete_handler(template, path, schema, table_name, fields):
    filepath = os.path.join(path, "delete_handler.py")
    
    context = {
        "table_name": table_name,
        "class_name": "".join([l.title() for l in table_name.split("_")]),
        "fields": fields,
    }

    template.stream(context).dump(open(filepath, "w"))


def make_read_handler(template, path, schema, table_name, fields):
    filepath = os.path.join(path, "read_handler.py")
    
    context = {
        "table_name": table_name,
        "class_name": "".join([l.title() for l in table_name.split("_")]),
        "fields": fields,
    }

    template.stream(context).dump(open(filepath, "w"))


def make_list_handler(template, path, schema, table_name, fields):
    filepath = os.path.join(path, "list_handler.py")
    
    context = {
        "table_name": table_name,
        "class_name": "".join([l.title() for l in table_name.split("_")]),
        "fields": fields,
    }

    template.stream(context).dump(open(filepath, "w"))


def make_crud(template_path, path, schema, table_name, fields):
    handlers_path = os.path.join(path, "handlers")

    if not os.path.exists(handlers_path):
        os.mkdir(handlers_path)
        open(os.path.join(handlers_path, "__init__.py"), "w").close()

    table_handlers_path = os.path.join(handlers_path, table_name)

    if not os.path.exists(table_handlers_path):
        os.mkdir(table_handlers_path)

    make_mixin.make_mixin(
        template_path, path, schema, table_name, fields)

    loader = FileSystemLoader(template_path)
    env = Environment(loader=loader)
    init_template = env.get_template("handlers/init.tpl")
    create_handler_template = env.get_template("handlers/create_handler.tpl")
    update_handler_template = env.get_template("handlers/update_handler.tpl")
    delete_handler_template = env.get_template("handlers/delete_handler.tpl")
    read_handler_template = env.get_template("handlers/read_handler.tpl")
    list_handler_template = env.get_template("handlers/list_handler.tpl")

    field_names = [field.get("name") for field in fields]

    make_init_handler(
        init_template, table_handlers_path, schema, table_name, field_names)

    make_create_handler(
        create_handler_template, table_handlers_path, schema, table_name, field_names)

    make_update_handler(
        update_handler_template, table_handlers_path, schema, table_name, field_names)

    make_delete_handler(
        delete_handler_template, table_handlers_path, schema, table_name, field_names)

    make_read_handler(
        read_handler_template, table_handlers_path, schema, table_name, field_names)

    make_list_handler(
        list_handler_template, table_handlers_path, schema, table_name, field_names)
