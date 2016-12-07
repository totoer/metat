#-*- coding: utf-8 -*-

import tornado.gen
import utils.validator
from sqlbuilder import *


{{ table_name_upper }}_SCHEMA = {
    {%- for field in fields %}
    "{{ field.get('name') }}": {% if field.get('type') == 'integer' %}{"type": "numeral", "required": True},{% else %}{"type": "string", "required": True, "empty": False},{% endif %}
    {%- endfor %}
}


class {{ class_name }}Mixin(object):

    @tornado.gen.coroutine
    def create_{{ table_name }}(self, data):
        v = utils.validator.ExtendValidator({{ table_name_upper }}_SCHEMA)

        if v.validete(data):
            cursor = yield self.db.execute(
                """insert into {{ schema }}.{{ table_name }}(
                    {%- for field in fields %}
                    {{ field.get('name') }}{% if fields.index(field) != fields_last_index %},{% else %}){% endif %}
                    {%- endfor %}
                values(
                    {%- for field in fields %}
                    %({{ field.get('name') }})s{% if fields.index(field) != fields_last_index %},{% else %}){% endif %}
                    {%- endfor %}
                returning id""", data)

            data["id"] = cursor.fetchone().get("id")

            raise tornado.gen.Return((data, None,))

        else:
            raise tornado.gen.Return((data, v.errors,))

    @tornado.gen.coroutine
    def update_{{ table_name }}(self, {{ table_name }}_id, data):
        v = utils.validator.ExtendValidator({{ table_name_upper }}_SCHEMA)

        if v.validete(data):
            data["{{ table_name }}_id"] = {{ table_name }}_id

            cursor = yield self.db.execute(
                """update {{ schema }}.{{ table_name }} set
                    {%- for field in fields %}
                    {{ field.get('name') }}=%({{ field.get('name') }})s{% if fields.index(field) != fields_last_index %},{% endif %}
                    {%- endfor %}
                where id=%({{ table_name }}_id)s""", data)

            raise tornado.gen.Return(None)

        else:
            raise tornado.gen.Return(v.errors)

    @tornado.gen.coroutine
    def get_{{ table_name }}(self, {{ table_name }}_id):
        query = SELECT()
        query.FROM("{{ schema }}", "{{ table_name }}")
        query.WHERE(
            C("{{ table_name }}", "id").EQUAL("%({{ table_name }}_id)s"))

        cursor = yield self.db.execute(query.sql, {
            "{{ table_name }}_id": {{ table_name }}_id,
        })

        raise tornado.gen.Return(cursor.fetchone())

    @tornado.gen.coroutine
    def get_{{ table_name }}_list(self, offset, limit):
        query = SELECT()
        query.FROM("{{ schema }}", "{{ table_name }}")
        query.OFFSET(offset)
        query.LIMIT(limit)

        cursor = yield self.db.execute(query.sql)

        raise tornado.gen.Return(cursor.fetchall())

    @tornado.gen.coroutine
    def delete_{{ table_name }}_list(self, {{ table_name }}_id):
        yield self.db.execute(
            "delete from {{ schema }}.{{ table_name }} where id=%s",
            ({{ table_name }}_id,))
