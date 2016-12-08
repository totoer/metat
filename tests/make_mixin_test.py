#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os

sys.path.append(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))

import test_env
import unittest
import make_mixin


TEST_RESULT = '''#-*- coding: utf-8 -*-

import tornado.gen
import utils.validator
from sqlbuilder import *


CUSTOMER_SCHEMA = {
    "id": {"type": "numeral", "required": True},
    "firstname": {"type": "string", "required": True, "empty": False},
    "lastname": {"type": "string", "required": True, "empty": False},
}


class CustomerMixin(object):

    @tornado.gen.coroutine
    def create_customer(self, data):
        v = utils.validator.ExtendValidator(CUSTOMER_SCHEMA)

        if v.validete(data):
            cursor = yield self.db.execute(
                """insert into customer.customer(
                    id,
                    firstname,
                    lastname)
                values(
                    %(id)s,
                    %(firstname)s,
                    %(lastname)s)
                returning id""", data)

            data["id"] = cursor.fetchone().get("id")

            raise tornado.gen.Return((data, None,))

        else:
            raise tornado.gen.Return((data, v.errors,))

    @tornado.gen.coroutine
    def update_customer(self, customer_id, data):
        v = utils.validator.ExtendValidator(CUSTOMER_SCHEMA)

        if v.validete(data):
            data["customer_id"] = customer_id

            cursor = yield self.db.execute(
                """update customer.customer set
                    id=%(id)s,
                    firstname=%(firstname)s,
                    lastname=%(lastname)s
                where id=%(customer_id)s""", data)

            raise tornado.gen.Return(None)

        else:
            raise tornado.gen.Return(v.errors)

    @tornado.gen.coroutine
    def get_customer(self, customer_id):
        query = SELECT()
        query.FROM("customer", "customer")
        query.WHERE(
            C("customer", "id").EQUAL("%(customer_id)s"))

        cursor = yield self.db.execute(query.sql, {
            "customer_id": customer_id,
        })

        raise tornado.gen.Return(cursor.fetchone())

    @tornado.gen.coroutine
    def get_customer_list(self, offset, limit):
        query = SELECT()
        query.FROM("customer", "customer")
        query.OFFSET(offset)
        query.LIMIT(limit)

        cursor = yield self.db.execute(query.sql)

        raise tornado.gen.Return(cursor.fetchall())

    @tornado.gen.coroutine
    def delete_customer_list(self, customer_id):
        yield self.db.execute(
            "delete from customer.customer where id=%s",
            (customer_id,))'''


class TestMakeMixin(unittest.TestCase):

    def test_make_mixin(self):
        tmp_path = test_env.make_tmp()

        fields = [
            {"name": "id", "type": "integer"},
            {"name": "firstname", "type": "text"},
            {"name": "lastname", "type": "text"},
        ]

        make_mixin.make_mixin(
            "../templates", tmp_path,
            "customer", "customer", fields)

        result_filepath = os.path.join(tmp_path, "mixins", "customer_mixin.py")

        self.assertEqual(open(result_filepath, "r").read(), TEST_RESULT)

        test_env.clear_tmp()
        

if __name__ == '__main__':
    unittest.main()
