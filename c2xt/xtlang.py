import clang.cindex as clang
import sys

# globals (yuck)

TARGET_SHLIB_NAME = 'libfoo'

# big-ol' C -> xtlang primitive type mapping

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
}


def is_primitive_type(type):
    'is it a "primitive" type, from an xtlang perspective?'
    return type in keys(XTLANG_TYPE_DICT)


def format_type(type):
    if type.kind == clang.TypeKind.POINTER:
        depth = 1
        base_type = type.get_pointee()
        while base_type.kind == clang.TypeKind.POINTER:
            print(type.spelling)
            depth += 1
            base_type = base_type.get_pointee()
        return format_type(base_type) + ('*' * depth)

    if type.kind == clang.TypeKind.ELABORATED:
        return format_type(type.get_canonical())

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
        return_type = type.get_result()
        arg_types = [format_type(t) for t in type.argument_types()]
        return '[{},{}]*'.format(format_type(return_type), ",".join(arg_types))

    else:
        try:
            return XTLANG_TYPE_DICT[type.kind]
        except KeyError:
            print('Unknown base type: {}'.format(type.kind))
            raise


def format_bindval(name, type, value, docstring=""):
    return '(bind-val {0} {1} {2} "{3}")'.format(name, type, value, docstring)


def format_bindalias(name, type, value, docstring=""):
    return '(bind-alias {0} {1} {2} "{3}")'.format(name, type, value, docstring)


def format_bindtype(name, type, docstring=""):
    return '(bind-type {0} {1} "{2}")'.format(name, type, docstring)


def format_bindlib(name, type, docstring=""):
    return '(bind-lib {0} {1} {2} "{3}")'.format(TARGET_SHLIB_NAME, name, type, docstring)


def format_bindlibval(name, type, docstring=""):
    return '(bind-lib-val {0} {1} {2} "{3}")'.format(TARGET_SHLIB_NAME, name, type, docstring)


# enum is kindof a special case because each child is a separate bind-val,
# so it's higher-level than the others
def format_enum(enum_cursor):
    assert enum_cursor.kind in [clang.CursorKind.ENUM_DECL,
                                clang.CursorKind.ENUM_CONSTANT_DECL]
    enum_type = format_type(enum_cursor.enum_type)

    enum_bindval_strings = [format_bindval(c.spelling, enum_type, c.enum_value) for c in enum_cursor.get_children()]
    enum_bindval_strings.insert(0, format_bindalias(enum_cursor.spelling, enum_type, format_type(enum_cursor.type)))
    return enum_bindval_strings

# #define

def format_macro_definition(defn_cursor):
    assert defn_cursor.kind == clang.CursorKind.MACRO_DEFINITION
    token = list(defn_cursor.get_tokens())[1]
    print('token {} {}'.format(token.kind, token.spelling))

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


# mother-of-all dispatch function (TODO doesn't work yet)

def format_cursor(cursor):
    if cursor.kind in [clang.CursorKind.ENUM_DECL, clang.CursorKind.ENUM_CONSTANT_DECL]:
        return '\n'.join(format_enum(cursor))
    if cursor.kind == clang.CursorKind.MACRO_DEFINITION:
        return format_macro_definition(cursor)
    if cursor.kind == clang.CursorKind.VAR_DECL:
        return format_bindlibval(cursor.spelling, format_type(cursor.type))
    if cursor.kind == clang.CursorKind.STRUCT_DECL:
        return format_bindtype(cursor)
    if cursor.kind == clang.CursorKind.FUNCTION_DECL:
        return format_bindlib(cursor.spelling, format_type(cursor.type))
    # if cursor.kind == clang.CursorKind.TYPEDEF_DECL:
    #     return format_bindalias(cursor)
