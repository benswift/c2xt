# -*- coding: utf-8 -*-

from c2xt.c2xt import *
import c2xt.xtlang as xtlang
import io


def dump_info(cursor):
    for c in cursor.walk_preorder():
        try:
            print('{}:{}'.format(c.spelling, c.type.kind))
        except:
            print('{}:notype'.format(c.spelling))


class TestNanoVG:
    nvg = parse_file('tests/nanovg.h', [])

    def test_top_level_walk(self):
        cursors = [cursor for cursor in self.nvg.get_children() if cursor.spelling == 'NVGwinding']
        assert cursors

    def test_nvgwinding_enum(self):
        cursor = find_child(self.nvg, 'NVG_SOLID')
        assert cursor.enum_value == 1

    def test_nvgsolidity_enum(self):
        cursor = find_child(self.nvg, 'NVG_HOLE')
        assert cursor.enum_value == 2

    def test_enum_parse(self):
        cursor = find_child(self.nvg, 'NVGwinding')
        bind_vals = xtlang.format_enum(cursor)
        assert '(bind-val NVG_CCW i32 1 "")' in bind_vals and '(bind-val NVG_CW i32 2 "")' in bind_vals

    def test_nvg_align(self):
        cursor = find_child(self.nvg, 'NVGalign')
        bind_vals = xtlang.format_enum(cursor)
        assert '(bind-val NVG_ALIGN_MIDDLE i32 16 "")' in bind_vals

    def test_nvg_pi(self):
        cursor = find_child(self.nvg, 'NVG_PI')
        assert xtlang.format_macro_definition(cursor) == '(bind-val NVG_PI float 3.14159265358979323846264338327 "")'

    def test_NVGcolor(self):
        cursor = find_child(self.nvg, 'NVGcolor')
        dump_info(cursor)
        assert xtlang.format_type(cursor) == '<float,float,float,float>'

    def test_NVGglyphPosition(self):
        cursor = find_child(self.nvg, 'NVGglyphPosition')
        dump_info(cursor)
        assert xtlang.format_type(cursor) == '<i8*,float,float,float>'
