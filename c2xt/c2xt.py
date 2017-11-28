#!/usr/bin/env python
# -*- coding: utf-8 -*-

import site
import os

LLVM_LIB_PATH = '/usr/local/opt/llvm/lib'
site.addsitedir(os.path.join(LLVM_LIB_PATH, 'python2.7', 'site-packages'))

try:
    import clang.cindex as clang
    clang.Config.set_library_path(LLVM_LIB_PATH)
except ImportError:
    print('Error: could not find LLVM python bindings')
    exit(1)


import external
import xtlang
import sys


# utilities

def parse_code_string(code_string):
    unsaved_files = [('xtlang_fragment.c', code_string)]
    tu = clang.TranslationUnit.from_source('xtlang_fragment.c', unsaved_files)
    return tu.cursor


def parse_file(filename, pp_definitions):
    tu = clang.TranslationUnit.from_source(filename, args=pp_definitions)
    return tu.cursor


def find_child(cursor, name):
    for c in cursor.walk_preorder():
        if c.spelling == name:
            return c
    raise NameError('no child cursor with name "{}" found'.format(name))


def in_stdlib(filename):
    return filename.startswith('/usr/include/') or filename.startswith('/System/')

def process_file(filename, libname, outfile, pp_definitions, pre_defined_types, opaque_types):
    main_cursor = parse_file(filename, pp_definitions)
    names = []
    for c in main_cursor.get_children():
        if c.spelling in names:
            pass # ignore the things already seen
        elif c.spelling in pre_defined_types.keys():
            print(pre_defined_types[c.spelling], file=outfile)
            names.append(c.spelling)
        elif in_stdlib(c.location.file.name):
            pass # ignore anything in the C standard library
        elif c.spelling in opaque_types:
            print(xtlang.format_bindalias(c.spelling, "i8"), file=outfile)
            names.append(c.spelling)
        else:
            print(xtlang.format_cursor(c, libname), file=outfile)
            names.append(c.spelling)


if __name__ == '__main__':
    external.process_nanovg()
