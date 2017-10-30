# -*- coding: utf-8 -*-

from c2xt.c2xt import *

class TestNanoVG:
    nvg = cursor_from_file('tests/nanovg.h', [])

    def test_top_level_walk(self):
        cursors = [cursor for cursor in self.nvg.get_children() if cursor.spelling == 'NVGwinding']
        assert cursors

    def test_nvgwinding_enum(self):
        cursor = cursor_with_name(self.nvg, 'NVG_SOLID')
        assert cursor.enum_value == 1

    def test_nvgsolidity_enum(self):
        cursor = cursor_with_name(self.nvg, 'NVG_HOLE')
        assert cursor.enum_value == 2

    # def test_nvgcolor_struct():
    #     cursor = cursor_with_name(nvg, 'NVGcolor')
    #     print(cursor.type.spelling)
    #     assert False
