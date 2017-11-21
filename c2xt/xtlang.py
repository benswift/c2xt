import clang.cindex as clang
import sys

XTLANG_TYPE_DICT = {
    clang.TypeKind.VOID: 'void',
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
    clang.TypeKind.NULLPTR: 'null',
    # clang.TypeKind.POINTER: 'i8*'
    clang.TypeKind.ENUM: 'i32'
    # clang.TypeKind.TYPEDEF: ''
    # clang.TypeKind.FUNCTIONPROTO: ''
}


def xtlang_type(cursor):
    return XTLANG_TYPE_DICT.get(cursor.kind)


def format_bindval(name, type, value, docstring=""):
    return '(bind-val {0} {1} {2} "{3}")'.format(name, type, value, docstring)


def format_bindalias(name, type, value, docstring=""):
    return '(bind-alias {0} {1} {2} "{3}")'.format(name, type, value, docstring)


def format_bindtype(name, type, docstring=""):
    return '(bind-type {0} {1} "{2}")'.format(name, type, docstring)


def format_bindlib(library, name, type, docstring=""):
    return '(bind-lib {0} {1} {2} "{3}")'.format(library, name, type, docstring)


def format_bindlibval(library, name, type, docstring=""):
    return '(bind-lib-val {0} {1} {2} "{3}")'.format(library, name, type, docstring)


# enums

def format_enum(enum_cursor):
    type_string = xtlang_type(enum_cursor.enum_type)
    for en in cursor.get_children():
        format_bindval(en.spelling, type_string, en.enum_value)


# #define

def format_macro_definition(defn_cursor):
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
        format_bindval(cursor.spelling, type_string, value)


# mother-of-all dispatch function (TODO doesn't work yet)

def format_cursor(cursor):
    if cursor.kind == clang.CursorKind.var_DECL:
        return format_bindlibval(cursor)
    if cursor.kind == clang.CursorKind.STRUCT_DECL:
        return format_bindtype(cursor)
    if cursor.kind in [clang.CursorKind.ENUM_DECL,
                       clang.CursorKind.ENUM_CONSTANT_DECL,
                       clang.CursorKind.MACRO_DEFINITION]:
        return format_bindval(cursor)
    if cursor.kind == clang.CursorKind.FUNCTION_DECL:
        return format_bindlib(cursor)
    if cursor.kind == clang.CursorKind.TYPEDEF_DECL:
        return format_bindalias(cursor)
