#-*- coding: utf-8 -*-

import torando.gen
import handlers.base_handler
import mixins.{{ table_name }}_mixin


class UpdateHandler(
        handlers.base_handler.BaseHandler,
        mixins.{{ table_name }}_mixin.{{ class_name }}Mixin):

    @tornado.gen.coroutine
    def get(self):
        {{ table_name }}_id = self.get_argument("{{ table_name }}_id", None)
        {{ table_name }} = yield self.get_{{ table_name }}({{ table_name }}_id)

        if {{ table_name }} is not None:
            self.render(
                "{{ table_name }}/update.html",
                data={{ table_name }}, errors=None)

        else:
            self.send_error(500)

    @tornado.gen.coroutine
    def post(self):
        {{ table_name }}_id = self.get_argument("{{ table_name }}_id", None)
        {{ table_name }} = yield self.get_{{ table_name }}({{ table_name }}_id)

        if {{ table_name }} is not None:
            errors = yield self.update_{{ table_name }}({{ table_name_id }}, {
                {%- for field in fields %}
                "{{ field }}": self.get_argument("{{ field }}", None),
                {%- endfor %}
            })

            if errors is not None:
                self.render(
                    "{{ table_name }}/update.html",
                    data={{ table_name }}, errors=errors)

            else:
                self.redirect("/{{ table_name }}/list")

        else:
            self.send_error(500)
