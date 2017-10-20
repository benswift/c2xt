import clang.cindex

XTLANG_TYPE_DICT = {
    clang.cindex.TypeKind.VOID: 'void',
    clang.cindex.TypeKind.BOOL: 'i1',
    clang.cindex.TypeKind.CHAR_U: 'i8',
    clang.cindex.TypeKind.UCHAR: 'i8',
    clang.cindex.TypeKind.CHAR16: 'i16',
    clang.cindex.TypeKind.CHAR32: 'i32',
    clang.cindex.TypeKind.USHORT: 'i16',
    clang.cindex.TypeKind.UINT: 'i32',
    clang.cindex.TypeKind.ULONG: 'i32',
    clang.cindex.TypeKind.ULONGLONG: 'i64',
    clang.cindex.TypeKind.CHAR_S: 'i8',
    clang.cindex.TypeKind.SCHAR: 'i8',
    clang.cindex.TypeKind.WCHAR: 'i16',
    clang.cindex.TypeKind.SHORT: 'i16',
    clang.cindex.TypeKind.INT: 'i32',
    clang.cindex.TypeKind.LONG: 'i32',
    clang.cindex.TypeKind.LONGLONG: 'i64',
    clang.cindex.TypeKind.FLOAT: 'float',
    clang.cindex.TypeKind.DOUBLE: 'double',
    clang.cindex.TypeKind.NULLPTR: 'null',
    # clang.cindex.TypeKind.POINTER: 'i8*'
    clang.cindex.TypeKind.ENUM: 'i32'
    # clang.cindex.TypeKind.TYPEDEF: ''
    # clang.cindex.TypeKind.FUNCTIONPROTO: ''
}


def xtlang_type_from_cursor(cursor):
    XTLANG_TYPE_DICT.get(cursor.kind)


class Alias(object):
    """an xtlang alias"""

    def __init__(self, cursor):
        self.name = cursor.spelling
        self.pretty_type = cursor.type.spelling
        self.docstring = ""

    def __str__(self):
        return '(bind-alias {} {} "{}")'.format(self.name,
                                                self.pretty_type,
                                                self.docstring)


class NamedType(object):
    """an xtlang named type"""

    def __init__(self, name, pretty_type, docstring=""):
        self.name = name
        self.pretty_type = pretty_type
        self.docstring = docstring

    def __str__(self):
        return '(bind-type {} {} "{}")'.format(self.name,
                                               self.pretty_type,
                                               self.docstring)


class GlobalVar(object):
    """an xtlang global variable"""

    def __init__(self, name, pretty_type, docstring=""):
        self.name = name
        self.pretty_type = pretty_type
        self.docstring = docstring

    def __str__(self):
        return '(bind-val {} {} "{}")'.format(self.name,
                                              self.pretty_type,
                                              self.docstring)


class LibraryFunction(object):
    """an xtlang library function"""

    def __init__(self, library, cursor):
        self.library = library
        self.name = cursor.spelling
        # self.pretty_type = pretty_type
        self.docstring = ""

    def __str__(self):
        return '(bind-lib {} {} {} "{}")'.format(self.library,
                                                 self.name,
                                                 self.pretty_type,
                                                 self.docstring)
