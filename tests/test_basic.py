# -*- coding: utf-8 -*-

from c2xt.c2xt import *
import c2xt.xtlang as xtlang
import io


def get_test_cursor(code_string, symbol_name):
    return find_child(parse_code_string(code_string), symbol_name)


def dump_info(cursor):
    for c in cursor.walk_preorder():
        try:
            print('{}:{}'.format(c.spelling, c.type.kind))
        except:
            print('{}:notype'.format(c.spelling))


class TestBasicC:

    def test_int_declaration(self):
        cursor = get_test_cursor('int ben = 32;', 'ben')
        assert cursor.spelling == 'ben'

    def test_macro_float_literal(self):
        cursor = get_test_cursor('#define FLOAT_CONST 2.65464f', 'FLOAT_CONST')
        assert xtlang.format_macro_definition(cursor) == '(bind-val FLOAT_CONST float 2.65464 "")'

    def test_macro_double_literal(self):
        cursor = get_test_cursor('#define DOUBLE_CONST 2.6544', 'DOUBLE_CONST')
        assert xtlang.format_macro_definition(cursor) == '(bind-val DOUBLE_CONST double 2.6544 "")'

    def test_macro_int_literal(self):
        cursor = get_test_cursor('#define INT_CONST 24', 'INT_CONST')
        assert xtlang.format_macro_definition(cursor) == '(bind-val INT_CONST i32 24 "")'

    # not sure how best to deal with different 'sizes' of #define constants
    # def test_macro_long_int_literal(self):
    #     cursor = get_test_cursor('#define LONG_INT_CONST 24ULL', 'LONG_INT_CONST')
    #     assert xtlang.format_macro_definition(cursor) == '(bind-val LONG_INT_CONST i64 54 "")'

    # def test_function_proto(self):
    #     cursor = get_test_cursor('int main(int argc, char[] *argv);', 'main')
    #     assert xtlang.format_function(cursor, 'libtest') == '(bind-lib main [i32,i32,i8**] "")'


class TestXtlangTypes:

    def test_array(self):
        cursor = get_test_cursor('int[10] ben;', 'ben')
        assert xtlang.xtlang_type(cursor.type) == '|10,i32|'


    def test_nested_array_struct(self):
        cursor = get_test_cursor('struct ben { int[2] arr; };', 'ben')
        assert xtlang.xtlang_type(cursor.type) == '<|2,i32|>'


    def test_nested_struct_array(self):
        cursor = get_test_cursor('struct point { int x; int y; }; struct point[5] ben;', 'ben')
        dump_info(cursor)
        assert xtlang.xtlang_type(cursor.type) == '|5,<i32,i32>|'


    def test_one_element_struct(self):
        cursor = get_test_cursor('struct ben { int x; };', 'ben')
        assert xtlang.xtlang_type(cursor.type) == '<i32>'


    def test_two_element_struct(self):
        cursor = get_test_cursor('struct ben { int x; float y; };', 'ben')
        assert xtlang.xtlang_type(cursor.type) == '<i32,float>'


    def test_nested_struct(self):
        cursor = get_test_cursor('struct point { int x; int y;}; struct ben { struct point p; float size; }', 'ben')
        assert xtlang.xtlang_type(cursor.type) == '<<i32,i32>,float>'


    def test_anon_inner_struct(self):
        cursor = get_test_cursor('struct ben { struct { float x, y; }; int jiblet; }', 'ben')
        assert xtlang.xtlang_type(cursor.type) == '<<float,float>,i32>'


    def test_pointer(self):
        cursor = get_test_cursor('int *ben;', 'ben')
        assert xtlang.xtlang_type(cursor.type) == 'i32*'


    def test_double_pointer(self):
        cursor = get_test_cursor('float **ben;', 'ben')
        assert xtlang.xtlang_type(cursor.type) == 'float**'


    def test_function_args(self):
        cursor = get_test_cursor('int main(int argc, char *argv[]);', 'main')
        assert xtlang.format_function(cursor, 'testlib') == '(bind-lib testlib main [i32,i32,i8**]* "")'
