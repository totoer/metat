#-*- coding: utf-8 -*-

import tornado.gen
import handlers.base_handler
import mixins.{{ table_name }}_mixin
import mixins.list_handler_mixin


class ListHandler(
        handlers.base_handler.BaseHandler,
        mixins.{{ table_name }}_mixin.{{ class_name }}Mixin,
        mixins.list_handler_mixin):

    @tornado.gen.coroutine
    def get(self):
        {{ table_name }}_list = yield self.get_{{ table_name }}_list(
            self.offset, self.limit)

        if self.offset == 0:
            self.render(
                "{{ table_name }}/list.html",
                {{ table_name }}_list={{ table_name }}_list)

        elif self.offset > 0 and len({{ table_name }}_list) > 0:
            self.render(
                "{{ table_name }}/items.html",
                {{ table_name }}_list={{ table_name }}_list)

        else:
            self.set_status(204)
