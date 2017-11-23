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


def process_header_file(filename, libname, outfile, pp_definitions, opaques):
    main_cursor = parse_file(filename, pp_definitions)
    names = []
    for c in main_cursor.get_children():
        if c.spelling in names:
            print('Warning: already seen {}, ignoring new {}'.format(c.spelling, c.type.kind))
        elif c.spelling in opaques:
            print(xtlang.format_bindalias(c.spelling, "i8*"), file=outfile)
            names.append(c.spelling)
        else:
            print(xtlang.format_cursor(c, libname), file=outfile)
            names.append(c.spelling)


def main():
    try:
        # ./c2xt.py infile [outfile preprocessor_definitions ...]
        with open(sys.argv[2], 'w') as outfile:
            process_header_file(sys.argv[1], outfile, sys.argv[3:], [], [])
        exit(0)
    except Exception as err:
        print(err)
        exit(1)


def process_nanovg():
    with open('tests/nanovg.xtm', 'w') as outfile:
        print(xtlang.output_header('nanovg', 'Ben Swift', 'TODO'), file=outfile)
        process_header_file('tests/nanovg.h', 'libnanovg', outfile, [], ['NVGcontext'])


if __name__ == '__main__':
    # main()
    process_nanovg()
