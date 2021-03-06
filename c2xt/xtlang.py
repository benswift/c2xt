import clang.cindex as clang
import sys
import datetime

# big-ol' C -> xtlang primitive type mapping

XTLANG_TYPE_DICT = {
    clang.TypeKind.VOID: 'i8',
    clang.TypeKind.BOOL: 'i1',
    clang.TypeKind.CHAR_U: 'i8',
    clang.TypeKind.UCHAR: 'i8',
    clang.TypeKind.CHAR16: 'i16',
    clang.TypeKind.CHAR32: 'i32',
    clang.TypeKind.USHORT: 'i16',
    clang.TypeKind.UINT: 'i32',
    clang.TypeKind.ULONG: 'i32',
    clang.TypeKind.ULONGLONG: 'i64',
    clang.TypeKind.CHAR_S: 'i8',
    clang.TypeKind.SCHAR: 'i8',
    clang.TypeKind.WCHAR: 'i16',
    clang.TypeKind.SHORT: 'i16',
    clang.TypeKind.INT: 'i32',
    clang.TypeKind.LONG: 'i32',
    clang.TypeKind.LONGLONG: 'i64',
    clang.TypeKind.FLOAT: 'float',
    clang.TypeKind.DOUBLE: 'double',
    clang.TypeKind.LONGDOUBLE: 'double',
    clang.TypeKind.NULLPTR: 'null',
    # clang.TypeKind.POINTER: 'i8*'
    clang.TypeKind.ENUM: 'i32'
}


def is_primitive_type(type):
    'is it a "primitive" type, from an xtlang perspective?'
    return type in keys(XTLANG_TYPE_DICT)


def pointer_depth(type):
    if type.kind == clang.TypeKind.POINTER:
        depth = 1
        base_type = type.get_pointee()
        while base_type.kind == clang.TypeKind.POINTER:
            depth += 1
            base_type = base_type.get_pointee()
        return depth
    # for non-pointers, just return 0
    else:
        return 0


def format_type(type):

    if type.kind == clang.TypeKind.POINTER:
        depth = 1
        base_type = type.get_pointee()
        while base_type.kind == clang.TypeKind.POINTER:
            depth += 1
            base_type = base_type.get_pointee()

        if base_type.kind == clang.TypeKind.UNEXPOSED:
            # i8* is xtlang's pointer to void
            return 'i8' + ('*' * depth)
        if base_type.get_declaration().kind == clang.CursorKind.NO_DECL_FOUND:
            return format_type(base_type) + ('*' * depth)
        else:
            return base_type.get_declaration().spelling + ('*' * depth)

    if type.kind == clang.TypeKind.ELABORATED:
        return format_type(type.get_canonical())

    if type.kind == clang.TypeKind.TYPEDEF:
        return type.spelling

    if type.kind == clang.TypeKind.CONSTANTARRAY:
        return '|{},{}|'.format(type.element_count, format_type(type.element_type))

    if type.kind == clang.TypeKind.INCOMPLETEARRAY:
        # in C, arrays are just pointers
        return format_type(type.element_type) + '*'

    if type.kind == clang.TypeKind.RECORD:
        member_types = [format_type(c.type) for c in type.get_fields()]
        return '<{}>'.format(",".join(member_types))

    # anonymous struct declarations
    if type.kind == clang.CursorKind.STRUCT_DECL:
        return format_type(type.get_definition().type)

    if type.kind == clang.TypeKind.FUNCTIONPROTO:

        # return type
        return_type = type.get_result()
        if return_type.kind == clang.TypeKind.VOID:
            return_type_string = 'void'
        else:
            return_type_string = format_type(return_type)

        # argument type(s)
        arg_types = [format_type(t) for t in type.argument_types()]
        if arg_types:
            return '[{},{}]*'.format(return_type_string, ",".join(arg_types))
        else:
            return '[{}]*'.format(return_type_string)

    else:
        try:
            return XTLANG_TYPE_DICT[type.kind]
        except KeyError:
            raise KeyError('Unknown base type: {}'.format(type.kind))


def format_bindval(name, type, value, docstring=""):
    return '(bind-val {0} {1} #x{2:X} "{3}")'.format(name, type, value, docstring)


def format_bindalias(name, type, docstring=""):
    return '(bind-alias {0} {1} "{2}")'.format(name, type, docstring)


def format_bindtype(name, type, docstring=""):
    return '(bind-type {0} {1} "{2}")'.format(name, type, docstring)


def format_bindlib(libname, name, type, docstring=""):
    return '(bind-lib {0} {1} {2} "{3}")'.format(libname, name, type, docstring)


def format_bindlibval(libname, name, type, docstring=""):
    return '(bind-lib-val {0} {1} #x{2:X} "{3}")'.format(libname, name, type, docstring)


# enum is kindof a special case because each child is a separate bind-val,
# so it's higher-level than the others
def format_enum(enum_cursor):
    assert enum_cursor.kind in [clang.CursorKind.ENUM_DECL,
                                clang.CursorKind.ENUM_CONSTANT_DECL]
    enum_type = format_type(enum_cursor.enum_type)

    xtlang_defns = []
    # is it a named enum?
    if enum_cursor.spelling:
        xtlang_defns.append(format_bindalias(enum_cursor.spelling, enum_type, format_type(enum_cursor.type)))
        enum_type = enum_cursor.spelling

    # now figure out the enum values
    value = 0
    for c in enum_cursor.get_children():
        if c.enum_value:
            xtlang_defns.append(format_bindval(c.spelling, enum_type, c.enum_value))
        else:
            xtlang_defns.append(format_bindval(c.spelling, enum_type, value))
            value += 1

    return xtlang_defns

# #define

def format_macro_definition(defn_cursor):
    assert defn_cursor.kind == clang.CursorKind.MACRO_DEFINITION
    token = list(defn_cursor.get_tokens())[1]

    if token.kind == clang.TokenKind.LITERAL:

        if token.spelling.endswith('f'):
            type_string = 'float'
            value = token.spelling[:-1]
        elif '.' in token.spelling:
            type_string = 'double'
            value = token.spelling
        else:
            type_string = 'i32'
            value = token.spelling
        return format_bindval(defn_cursor.spelling, type_string, value)
    else:
        return None


# mother-of-all dispatch function

def format_cursor(cursor, libname):

    if cursor.kind in [clang.CursorKind.ENUM_DECL, clang.CursorKind.ENUM_CONSTANT_DECL]:
        return '\n'.join(format_enum(cursor))

    if cursor.kind == clang.CursorKind.MACRO_DEFINITION:
        return format_macro_definition(cursor)

    if cursor.kind == clang.CursorKind.VAR_DECL:
        return format_bindlibval(libname, cursor.spelling, format_type(cursor.type))

    if cursor.kind == clang.CursorKind.STRUCT_DECL:
        docstring = '\n'.join(['@member {} - index {}'.format(c.spelling, i) for (i, c) in enumerate(cursor.get_children())])
        return format_bindtype(cursor.spelling, format_type(cursor.type), docstring)

    if cursor.kind == clang.CursorKind.FUNCTION_DECL:
        docstring = '\n'.join(['@param {} - index {}'.format(c.spelling, i) for (i, c) in enumerate(cursor.get_children())])
        return format_bindlib(libname, cursor.spelling, format_type(cursor.type), docstring)

    if cursor.kind == clang.CursorKind.TYPEDEF_DECL:
        return format_bindalias(cursor.spelling, format_type(cursor.underlying_typedef_type))


def output_header(libname, author, comment, deps=[]):
    deps.insert(0, 'libs/base/base.xtm')
    suppress_aot_deps = '\n '.join(['(sys:load "{}")'.format(dep) for dep in deps])
    insert_forms_deps = '\n '.join(['(sys:load "{}" \'quiet)'.format(dep) for dep in deps])
    deps_string = """(impc:aot:suppress-aot-do
 {})
(impc:aot:insert-forms
 {})""".format(suppress_aot_deps, insert_forms_deps)

    return """;;; {0}.xtm -- {0} bindings for Extempore

;; Author: {1}
;; Keywords: extempore
;; Required dylibs: lib{0}

;;; Commentary:

;; {2}

;; These bindings were automatically generated by c2xt.py on {3:%Y-%m-%d}

;;; Code:

(sys:load "libs/aot-cache/{0}.xtm" 'quiet)
(sys:load-preload-check '{0})
(define *xtmlib-{0}-loaded* #f)

{4}

(impc:aot:insert-header "xtm{0}")

;; set up the current dylib name and path (for AOT compilation)
(bind-dylib lib{0}
  (cond ((string=? (sys:platform) "OSX")
         "lib{0}.dylib")
        ((string=? (sys:platform) "Linux")
         "lib{0}.so")
        ((string=? (sys:platform) "Windows")
         "{0}.dll")))
""".format(libname, author, comment, datetime.datetime.now(), deps_string)


def output_footer(libname, path, scm_file=False):

    footer = """(impc:aot:insert-footer "xtm{0}")
(define *xtmlib-{0}-loaded* #t)
""".format(libname)

    # if there's gonna be a scheme file, append it to the footer
    if scm_file:
        footer = '(sys:load "{}/{}-scm.xtm")\n{}'.format(path, libname, footer)

    return footer
