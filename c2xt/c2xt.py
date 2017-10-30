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


def emit(cursor, file=sys.stdout):
    if cursor.kind == clang.CursorKind.var_DECL:
        return xtlang.format_bindlibval(cursor)
    if cursor.kind == clang.CursorKind.STRUCT_DECL:
        return xtlang.format_bindtype(cursor)
    if cursor.kind in [clang.CursorKind.ENUM_DECL,
                       clang.CursorKind.ENUM_CONSTANT_DECL,
                       clang.CursorKind.MACRO_DEFINITION]:
        return xtlang.format_bindval(cursor)
    if cursor.kind == clang.CursorKind.FUNCTION_DECL:
        return xtlang.format_bindlib(cursor)
    if cursor.kind == clang.CursorKind.TYPEDEF_DECL:
        return xtlang.format_bindalias(cursor)


def process_file(filename, pp_definitions=[]):
    main_cursor = parse_file(filename, pp_definitions)
    for c in main_cursor.get_children():
        emit(c)


if __name__ == '__main__':
    try:
        process_file(sys.argv[1], sys.argv[2:])
        exit(0)
    except Exception as err:
        print(err)
        exit(1)
