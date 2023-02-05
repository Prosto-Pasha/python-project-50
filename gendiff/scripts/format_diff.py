BLANK_STR = '    '
PLUS_STR = '  + '
MINUS_STR = '  - '
MINUS_PLUS_STR = ' -+ '


def get_args_str(arg1, arg2, indent):
    """
    Возвращает строковое представление
    аргументов arg1 и arg2 для
    типа различия diff_type
    с учетом отступа indent
    в формате  stylish
    """
    arg1_str = None if arg1 is None else get_stylish(arg1, indent + 1)
    arg2_str = None if arg2 is None else get_stylish(arg2, indent + 1)
    return arg1_str, arg2_str


def get_list_items(arg1_str, arg2_str, diff_type, indent_str, key_str):
    """
    Возвращает элементы для списка различий
    в формате  stylish
    """
    arg1_list_item = None
    arg2_list_item = None
    start_str = f'{indent_str}{diff_type}{key_str}: '
    if diff_type == BLANK_STR:
        arg1_list_item = f'{start_str}{arg1_str}'
    elif diff_type == PLUS_STR:
        arg2_list_item = f'{start_str}{arg2_str}'
    elif diff_type == MINUS_STR:
        arg1_list_item = f'{start_str}{arg1_str}'
    elif diff_type == MINUS_PLUS_STR:
        arg1_list_item = f'{indent_str}{MINUS_STR}{key_str}: {arg1_str}'
        arg2_list_item = f'{indent_str}{PLUS_STR}{key_str}: {arg2_str}'
    return arg1_list_item, arg2_list_item


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
            diff_type = arg[0]  # ''  '-'  '+'  '-+'
            key_str = arg[1]
            arg1_str, arg2_str = get_args_str(
                arg[2],
                arg[3],
                indent
            )
            arg1_list_item, arg2_list_item = get_list_items(
                arg1_str,
                arg2_str,
                diff_type,
                indent_str,
                key_str
            )
            if arg1_list_item is not None:
                result.append(arg1_list_item)
            if arg2_list_item is not None:
                result.append(arg2_list_item)
    result.append(f'{indent_str}}}')
    result = '\n'.join(result)
    return result


def get_value_str(arg):
    """
    Возвращает текстовое представление
    значения аргумента arg
    в формате plain
    """
    if isinstance(arg, dict):
        return '[complex value]'
    if arg in ('true', 'false', 'null'):
        return arg
    return f"'{arg}'"


def get_arg1_arg2_str(diff_type, arg1, arg2):
    """
    Возвращает строку по типу различия
    для двух аргументов
    в формате plain
    """
    result = ''
    if diff_type == PLUS_STR:
        middle_text = 'was added with value:'
        value_str = get_value_str(arg2)
        result = f'{middle_text} {value_str}'
    elif diff_type == MINUS_STR:
        result = 'was removed'
    else:  # diff_type == MINUS_PLUS_STR:
        middle_text = 'was updated. From'
        value_str_arg1 = get_value_str(arg1)
        value_str_arg2 = get_value_str(arg2)
        result = f'{middle_text} {value_str_arg1} to {value_str_arg2}'
    return result


def get_list_item(arg, path):
    """
    Возвращает строковое представление одного отличия
    в формате plain
    """
    diff_type = arg[0]
    current_path = arg[1]
    arg1 = arg[2]
    arg2 = arg[3]
    if path:
        path = f'{path}.{current_path}'
    else:
        path = current_path
    if diff_type == BLANK_STR and isinstance(arg1, list):
        return get_plain(arg1, path)
    if diff_type == BLANK_STR:
        return None
    arg1_arg2_str = get_arg1_arg2_str(diff_type, arg1, arg2)
    return f"Property '{path}' {arg1_arg2_str}"


def get_plain(diff_l, path=''):
    """
    Возвращает строковое представление
    по списку различий двух словарей
    в формате plain
    """
    result = []
    is_list = isinstance(diff_l, list)
    is_dict = isinstance(diff_l, dict)
    if is_dict:
        return '[complex value]'
    if not is_list:
        return str(diff_l)
    if is_list:
        for arg in diff_l:
            list_item = get_list_item(arg, path)
            if list_item is not None:
                result.append(list_item)
    result = '\n'.join(result)
    return result


def get_diff_string(diff_l, format):
    """
    Возвращает строковое представление
    по списку различий двух словарей
    в нужном формате
    """
    return get_stylish(diff_l)\
        if format == 'stylish'\
        else get_plain(diff_l)
