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


def update_result_from_list(diff_l, indent, result):
    """
    Добавляет в список result изменения из diff_l
    с учётом отступа indent
    в формате  stylish
    """
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
            BLANK_STR * indent,
            key_str
        )
        if arg1_list_item is not None:
            result.append(arg1_list_item)
        if arg2_list_item is not None:
            result.append(arg2_list_item)


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
    if is_list:
        update_result_from_list(diff_l, indent, result)
    result.append(f'{BLANK_STR * indent}}}')
    result = '\n'.join(result)
    return result
