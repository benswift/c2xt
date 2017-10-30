# -*- coding: utf-8 -*-

import clang.cindex as clang
import c2xt.xtlang as xtlang

def cursor_from_code_string(code_string):
    tu = clang.TranslationUnit.from_source(
        'xtlang_fragment.c',
        unsaved_files=[('xtlang_fragment.c', code_string)],
        options=clang.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
    )
    return tu.cursor


def cursor_from_file(filename, pp_definitions=[]):
    tu = clang.TranslationUnit.from_source(
        filename,
        args=pp_definitions,
        options=clang.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
    )
    return tu.cursor


def cursor_with_name(tu, name):
    for cursor in tu.walk_preorder():
        if cursor.spelling == name:
            return cursor
    raise NameError('no cursor with name "{}" found'.format(name))


if __name__ == '__main__':
    try:
        process_file(sys.argv[1], sys.argv[2:])
        exit(0)
    except Exception as err:
        print(err)
        exit(1)
