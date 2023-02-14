from gendiff.format_scripts.format_common import format_arg


DIFF_TYPE = {
    'added': '  + ',
    'removed': '  - ',
    'unchanged': '    ',
    'nested': '    ',
    'changed': ' -+ ',
}
BLANK_STR = '    '


def get_args_str(arg1, arg2, indent):
    """
    Возвращает строковое представление
    аргументов arg1 и arg2 для
    типа различия diff_type
    с учетом отступа indent
    в формате  stylish
    """
    arg1_str = get_stylish(arg1, indent + 1)
    arg2_str = get_stylish(arg2, indent + 1)
    return arg1_str, arg2_str


def get_list_items(args, diff_type, indent_str, key_str):
    """
    Возвращает элементы для списка различий
    в формате stylish
    """
    arg1_str = args[0]
    arg2_str = args[1]
    arg1_list_item = None
    arg2_list_item = None
    diff = DIFF_TYPE[diff_type]
    single_str = f'{indent_str}{diff}{key_str}: '
    if diff_type == 'changed':
        arg1_list_item = f'{indent_str}  - {key_str}: {arg1_str}'
        arg2_list_item = f'{indent_str}  + {key_str}: {arg2_str}'
    elif diff_type == 'added':
        arg2_list_item = f'{single_str}{arg2_str}'
    else:
        arg1_list_item = f'{single_str}{arg1_str}'
    return arg1_list_item, arg2_list_item


def update_result_from_list(diff_l, indent, result):
    """
    Добавляет в список result изменения из diff_l
    с учётом отступа indent
    в формате  stylish
    """
    for arg in diff_l:
        diff_type = arg[0]
        key_str = arg[1]
        args = get_args_str(
            arg[2],
            arg[3],
            indent
        )
        arg1_list_item, arg2_list_item = get_list_items(
            args,
            diff_type,
            BLANK_STR * indent,
            key_str
        )
        if arg1_list_item is not None:
            result.append(arg1_list_item)
        if arg2_list_item is not None:
            result.append(arg2_list_item)


def format_sub_tree(diff_l, indent):
    """
    Обработка сложного листа
    """
    result = []
    update_result_from_list(diff_l, indent, result)
    result.append(f'{BLANK_STR * indent}}}')
    result.insert(0, '{')
    result = '\n'.join(result)
    return result


def format_complex_leaf(diff_l, indent):
    """
    Обработка вложенного дерева
    """
    result = []
    for key, arg in diff_l.items():
        start_str = BLANK_STR * (indent + 1)
        arg_str = get_stylish(arg, indent + 1)
        result.append(f'{start_str}{key}: {arg_str}')
    result.append(f'{BLANK_STR * indent}}}')
    result.insert(0, '{')
    result = '\n'.join(result)
    return result


def format_leaf(diff_l, indent):
    """
    Обработка простого листа
    """
    return format_arg(diff_l)


def get_stylish(diff_l, indent=0):
    """
    Возвращает строковое представление
    по списку различий двух словарей
    в формате stylish
    """
    FORMAT_FUNC = {
        'format_sub_tree': format_sub_tree,
        'format_complex_leaf': format_complex_leaf,
        'format_leaf': format_leaf
    }
    if isinstance(diff_l, list):
        func_name = 'format_sub_tree'
    elif isinstance(diff_l, dict):
        func_name = 'format_complex_leaf'
    else:
        func_name = 'format_leaf'
    return FORMAT_FUNC[func_name](diff_l, indent)
