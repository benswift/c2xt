# -*- coding: utf-8 -*-

from c2xt.c2xt import *

def test_int_declaration():
    cursor = cursor_from_code_string("int ben = 32;")
    assert cursor.spelling == "ben"
