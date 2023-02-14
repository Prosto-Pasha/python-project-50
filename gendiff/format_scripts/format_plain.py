from gendiff.format_scripts.format_common import format_arg


def get_value_str(arg):
    """
    Возвращает текстовое представление
    значения аргумента arg
    в формате plain
    """
    if isinstance(arg, dict):
        return '[complex value]'
    if isinstance(arg, int) or isinstance(arg, bool) or arg is None:
        return format_arg(arg)
    return f"'{arg}'"


def get_arg1_arg2_str(diff_type, arg1, arg2):
    """
    Возвращает строку по типу различия
    для двух аргументов
    в формате plain
    """
    result = ''
    if diff_type == 'added':
        middle_text = 'was added with value:'
        value_str = get_value_str(arg2)
        result = f'{middle_text} {value_str}'
    elif diff_type == 'removed':
        result = 'was removed'
    else:  # diff_type == 'changed':
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
    if diff_type == 'nested':
        return get_plain(arg1, path)
    elif diff_type == 'unchanged':
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
    if isinstance(diff_l, dict):
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
