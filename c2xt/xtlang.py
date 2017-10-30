import clang.cindex as clang

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


def type_from_cursor(cursor):
    return XTLANG_TYPE_DICT.get(cursor.kind)


def format_bindalias(cursor):
    return '(bind-alias {0} {1} "{2}")'.format(cursor.spelling,
                                               cursor.type.spelling,
                                               "")


def format_bindtype(cursor):
    return '(bind-type {0} {1} "{2}")'.format(cursor.spelling,
                                              cursor.type.spelling,
                                              "")


def format_bindval(cursor):
    return '(bind-val {0} {1} "{2}")'.format(cursor.spelling,
                                             cursor.type.spelling,
                                             "")


def format_bindlib(cursor, library):
    return '(bind-lib {0} {1} "{2}")'.format(library,
                                             cursor.spelling,
                                             cursor.type.spelling,
                                             "")


def format_bindlibval(cursor, library):
    return '(bind-lib-val {0} {1} "{2}")'.format(library,
                                                 cursor.spelling,
                                                 cursor.type.spelling,
                                                 "")
