#-*- coding: utf-8 -*-

import cerberus


class ExtendValidator(cerberus.Validator):

    def _validate_type_numeral(self, value):
        if (isinstance(value, str) or isinstance(value, unicode)) \
                and value.isdigit():

            return True

        if not (isinstance(value, str) or isinstance(value, unicode)) and \
                isinstance(value, (int, long, float, complex)):

            return True
