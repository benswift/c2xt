# -*- coding: utf-8 -*-

from c2xt.c2xt import *

def test_int_declaration():
    cursor = parse_code_string("int ben = 32;")
    bencursor = find_child(cursor, "ben")
    assert bencursor.spelling == "ben"
