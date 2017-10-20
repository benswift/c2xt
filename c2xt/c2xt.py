# -*- coding: utf-8 -*-

# usage: c2xt.py filename.h -DDEFN_1 -DDEFN_2 ...

import sys
import site
site.addsitedir("/usr/local/opt/llvm/lib/python2.7/site-packages/")
import clang.cindex as cl
cl.Config.set_library_path("/usr/local/opt/llvm/lib/")
from xtlang import Alias, NamedType, GlobalVar, LibraryFunction



def cursor_from_code_string(code_string):
    tu = clang.cindex.TranslationUnit.from_source(
        'snippet.h',
        unsaved_files=[('snippet.h', code_string)],
        options=clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
    )
    return tu.cursor


def cursor_with_name(tu, name):
    for cursor in tu.cursor.walk_preorder():
        if cursor.spelling == name:
            return cursor

    return None



def process_file(filename, pp_definitions=[]):
    tu = clang.cindex.TranslationUnit.from_source(
        filename,
        args=pp_definitions,
        options=clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
    )

    # for cursor in tu.cursor.get_children():
    #     xtlang_from_cursor(cursor)


if __name__ == '__main__':
    process_file(sys.argv[1], sys.argv[2:])
    # sys.exit()
