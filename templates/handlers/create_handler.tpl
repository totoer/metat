#-*- coding: utf-8 -*-

import tornado.web
import tornado.gen
import handlers.base_handler
import mixins.{{ table_name }}_mixin


class CreateHandler(
        handlers.base_handler.BaseHandler,
        mixins.{{ table_name }}_mixin.{{ class_name }}Mixin):

    @tornado.web.asynchronous
    def get(self):
        self.render(
            "{{ table_name }}/create.html",
            data=None, errors=None)

    @tornado.gen.coroutine
    def post(self):
        data, errors = yield self.create_{{ table_name }}({
            {%- for field in fields %}
            "{{ field }}": self.get_argument("{{ field }}", None),
            {%- endfor %}
        })

        if errors is not None:
            self.render(
                "{{ table_name }}/create.html",
                data=data, errors=errors)

        else:
            self.redirect("/{{ table_name }}/list")
