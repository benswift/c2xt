# -*- coding: utf-8 -*-

import clang.cindex as clang
import c2xt.xtlang as xtlang
import sys

def parse_code_string(code_string):
    tu = clang.TranslationUnit.from_source(
        'xtlang_fragment.c',
        unsaved_files=[('xtlang_fragment.c', code_string)],
        options=clang.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
    )
    return tu.cursor


def parse_file(filename, pp_definitions):
    tu = clang.TranslationUnit.from_source(
        filename,
        args=pp_definitions,
        options=clang.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
    )
    return tu.cursor


def find_child(cursor, name):
    for c in cursor.walk_preorder():
        if c.spelling == name:
            return c
    raise NameError('no child cursor with name "{}" found'.format(name))


def process_file(filename, pp_definitions=[]):
    main_cursor = parse_file(filename, pp_definitions)
    for c in main_cursor.get_children():
        print(format_cursor(c))


if __name__ == '__main__':
    try:
        process_file(sys.argv[1], sys.argv[2:])
        exit(0)
    except Exception as err:
        print(err)
        exit(1)
