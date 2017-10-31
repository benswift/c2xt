# -*- coding: utf-8 -*-

from c2xt.c2xt import *
import c2xt.xtlang as xtlang
import io

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
        with io.StringIO() as out:
            type_string = xtlang.xtlang_type(cursor.enum_type)
            for en in cursor.get_children():
                xtlang.emit_bindval(en.spelling, type_string, en.enum_value, file=out)
            assert '(bind-val NVG_CCW i32 1 "")' in out.getvalue() and '(bind-val NVG_CW i32 2 "")' in out.getvalue()

    # def test_nvgcolor_struct():
    #     cursor = cursor_with_name(nvg, 'NVGcolor')
    #     print(cursor.type.spelling)
    #     assert False
