#-*- coding: utf-8 -*-

import tornado.gen
import handlers.base_handler
import mixins.{{ table_name }}_mixin


class DeleteHandler(
        handlers.base_handler.BaseHandler,
        mixins.{{ table_name }}_mixin.{{ class_name }}Mixin):

    @tornado.gen.coroutine
    def get(self):
        {{ table_name }}_id = self.get_argument("{{ table_name }}_id", None)
        {{ table_name }} = yield self.get_{{ table_name }}({{ table_name }}_id)

        if {{ table_name }} is not None:
            yield self.delete_{{ table_name }}({{ table_name }}.get('id'))

            self.redirect("/{{ table_name }}/list")

        else:
            self.send_error(500)
