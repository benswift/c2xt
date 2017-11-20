# -*- coding: utf-8 -*-

from c2xt.c2xt import *
import c2xt.xtlang as xtlang
import io

class TestBasicC:

    def test_int_declaration(self):
        cursor = find_child(parse_code_string("int ben = 32;"), "ben")
        assert cursor.spelling == "ben"
