#-*- coding: utf-8 -*-

import tornado.gen
import handlers.base_handler
import mixins.{{ table_name }}_mixin


class ReadHandler(
        handlers.base_handler.BaseHandler,
        mixins.{{ table_name }}_mixin.{{ class_name }}Mixin):

    @tornado.gen.coroutine
    def get(self):
        {{ table_name }}_id = self.get_argument("{{ table_name }}_id", None)
        {{ table_name }} = self.get_{{ table_name }}({{ table_name }}_id)

        if {{ table_name }} is not None:
            self.render(
                "{{ table_name }}/read.html",
                {{ table_name }}={{ table_name }})

        else:
            self.send_error(500)
