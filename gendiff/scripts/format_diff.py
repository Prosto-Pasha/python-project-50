BLANK_STR = '    '


def get_stylish(diff_l, indent=0):
    """
    Возвращает строковое представление
    по списку различий двух словарей
    в формате stylish
    """
    result = []
    is_list = isinstance(diff_l, list)
    is_dict = isinstance(diff_l, dict)
    if not is_list and not is_dict:
        return str(diff_l)
    result.append('{')
    if is_dict:
        for key, arg in diff_l.items():
            start_str = BLANK_STR * (indent + 1)
            arg_str = get_stylish(arg, indent + 1)
            result.append(f'{start_str}{key}: {arg_str}')
    indent_str = BLANK_STR * indent
    if is_list:
        for arg in diff_l:
            start_str = arg[0]
            key_str = arg[1]
            arg_str = get_stylish(arg[2], indent + 1)
            result.append(f'{indent_str}{start_str}{key_str}: {arg_str}')
    result.append(f'{indent_str}}}')
    result = '\n'.join(result)
    return result


def get_plain(diff_l, indent=0):
    """
    Возвращает строковое представление
    по списку различий двух словарей
    в формате plain
    """
    return ''


def get_diff_string(diff_l, format):
    """
    Возвращает строковое представление
    по списку различий двух словарей
    в нужном формате
    """
    return get_stylish(diff_l)\
        if format == 'stylish'\
        else get_plain(diff_l)
