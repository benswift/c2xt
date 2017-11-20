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


def emit_bindval(name, type, value, docstring="", file=sys.stdout):
    print ('(bind-val {0} {1} {2} "{3}")'.format(name,
                                                 type,
                                                 value,
                                                 docstring),
           file=file)


def emit_bindalias(name, type, value, docstring="", file=sys.stdout):
    print ('(bind-alias {0} {1} {2} "{3}")'.format(name,
                                                 type,
                                                 value,
                                                 docstring),
           file=file)


def emit_bindtype(name, type, docstring="", file=sys.stdout):
    print ('(bind-type {0} {1} "{2}")'.format(name,
                                              type,
                                              docstring),
           file=file)


def emit_bindlib(library, name, type, docstring="", file=sys.stdout):
    print ('(bind-lib {0} {1} {2} "{3}")'.format(library,
                                                 name,
                                                 type,
                                                 docstring),
           file=file)


def emit_bindlibval(library, name, type, docstring="", file=sys.stdout):
    print ('(bind-lib-val {0} {1} {2} "{3}")'.format(library,
                                                     name,
                                                     type,
                                                     docstring),
           file=file)


# enums

def process_enum(cursor):
    type_string = xtlang_type(cursor.enum_type)
    for en in cursor.get_children():
        emit_bindval(en.spelling, type_string, en.enum_value)


# macro definitions

def process_macro_definition(cursor):
    token = list(cursor.get_tokens())[1]

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
        emit_bindval(cursor.spelling, type_string, value)
