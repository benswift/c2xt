# -*- coding: utf-8 -*-

from c2xt.c2xt import *
import c2xt.xtlang as xtlang
import io

class TestBasicC:

    def test_int_declaration(self):
        cursor = find_child(parse_code_string('int ben = 32;'), 'ben')
        assert cursor.spelling == 'ben'

    def test_macro_float_literal(self):
        cursor = find_child(parse_code_string('#define FLOAT_CONST 2.65464f'), 'FLOAT_CONST')
        assert process_macro_definition(cursor) == '(bind-val FLOAT_CONST float 2.65464 "")'

    def test_macro_double_literal(self):
        cursor = find_child(parse_code_string('#define DOUBLE_CONST 2.6544'), 'DOUBLE_CONST')
        assert process_macro_definition(cursor) == '(bind-val DOUBLE_CONST double 2.6544 "")'

    def test_macro_int_literal(self):
        cursor = find_child(parse_code_string('#define INT_CONST 24'), 'INT_CONST')
        assert process_macro_definition(cursor) == '(bind-val INT_CONST i32 24 "")'

    def test_macro_long_int_literal(self):
        cursor = find_child(parse_code_string('#define LONG_INT_CONST 24ULL'), 'LONG_INT_CONST')
        assert process_macro_definition(cursor) == '(bind-val LONG_INT_CONST i64 54 "")'
