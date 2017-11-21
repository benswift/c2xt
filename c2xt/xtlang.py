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
}


def pointer_depth(type, depth):
    if type.kind == clang.TypeKind.POINTER:
        return pointer_depth(type.get_pointee(), depth+1)
    else:
        return depth


def xtlang_primitive_type(type):
    'is it a "primitive" type, from an xtlang perspective?'
    return type in keys(XTLANG_TYPE_DICT)


def format_constantarray(type):
    assert type.kind == clang.TypeKind.CONSTANTARRAY
    return '|{},{}|'.format(type.element_count, xtlang_type(type.element_type))


def format_struct(type):
    assert type.kind == clang.TypeKind.RECORD
    member_types = [xtlang_type(c.type) for c in type.get_fields()]
    return '<{}>'.format(",".join(member_types))


def format_closure(type):
    return_type = type.get_result()
    arg_types = [xtlang_type(t) for t in type.argument_types()]
    return '[{},{}]*'.format(xtlang_type(return_type), ",".join(arg_types))


def xtlang_type(type):
    if type.kind == clang.TypeKind.POINTER:
        depth = 1
        base_type = type.get_pointee()
        while base_type.kind == clang.TypeKind.POINTER:
            print(type.spelling)
            depth += 1
            base_type = base_type.get_pointee()
        return xtlang_type(base_type) + ('*' * depth)

    if type.kind == clang.TypeKind.ELABORATED:
        return xtlang_type(type.get_canonical())

    if type.kind == clang.TypeKind.CONSTANTARRAY:
        return format_constantarray(type)

    if type.kind == clang.TypeKind.INCOMPLETEARRAY:
        # in C, arrays are just pointers
        return xtlang_type(type.element_type) + '*'

    if type.kind == clang.TypeKind.RECORD:
        return format_struct(type)

    if type.kind == clang.CursorKind.STRUCT_DECL:
        return format_struct(type.get_definition().type)

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


def format_bindlib(library, name, type, docstring=""):
    return '(bind-lib {0} {1} {2} "{3}")'.format(library, name, type, docstring)


def format_bindlibval(library, name, type, docstring=""):
    return '(bind-lib-val {0} {1} {2} "{3}")'.format(library, name, type, docstring)



# enums

def format_enum(enum_cursor):
    assert enum_cursor.kind == clang.CursorKind.ENUM_DECL
    type_string = xtlang_type(enum_cursor.enum_type)

    enum_bindval_strings = [format_bindval(c.spelling, type_string, c.enum_value) for c in enum_cursor.get_children()]
    enum_bindval_strings.insert(0, format_bindalias(enum_cursor.spelling, type_string, xtlang_type(enum_cursor.type)))
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


# C functions

def format_function(function_cursor, libname):
    assert function_cursor.kind == clang.CursorKind.FUNCTION_DECL
    return format_bindlib(libname, function_cursor.spelling, format_closure(function_cursor.type))

# mother-of-all dispatch function (TODO doesn't work yet)

def format_cursor(cursor):
    if cursor.kind in [clang.CursorKind.ENUM_DECL, clang.CursorKind.ENUM_CONSTANT_DECL]:
        return format_enum(cursor)
    if cursor.kind == clang.CursorKind.MACRO_DEFINITION:
        return format_macro_definition(cursor)
    # if cursor.kind == clang.CursorKind.VAR_DECL:
    #     return format_bindlibval(cursor)
    # if cursor.kind == clang.CursorKind.STRUCT_DECL:
    #     return format_bindtype(cursor)
    # if cursor.kind == clang.CursorKind.FUNCTION_DECL:
    #     return format_bindlib(cursor)
    # if cursor.kind == clang.CursorKind.TYPEDEF_DECL:
    #     return format_bindalias(cursor)
