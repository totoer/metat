#-*- coding: utf-8 -*-

import create_handler
import update_handler
import delete_handler
import read_handler
import list_handler


urls = [
    (r"/{{ table_name }}/create/?", create_handler.CreateHandler,),
    (r"/{{ table_name }}/update/?", update_handler.UpdateHandler,),
    (r"/{{ table_name }}/delete/?", delete_handler.DeleteHandler),
    (r"/{{ table_name }}/read/?", read_handler.ReadHandler,),
    (r"/{{ table_name }}/list/?", list_handler.ListHandler,),
]