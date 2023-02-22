from gendiff.formatters.format_common import format_arg


DIFF_TYPE = {
    'added': '  + ',
    'removed': '  - ',
    'unchanged': '    ',
    'nested': '    ',
    'changed': ' -+ ',
}
BLANK_STR = '    '


def get_stylish(diff_l, indent=0):
    """
    Возвращает строковое представление
    по списку различий двух словарей
    в формате stylish
    """
    vertex_func = {
        'unchanged': format_unchanged,
        'added': format_added,
        'removed': format_removed,
        'nested': format_nested,
        'changed': format_changed}
    result = []
    for arg in diff_l:
        func = vertex_func[arg[0]]
        func(arg, indent, result)
    result.append(f'{BLANK_STR * indent}}}')
    result.insert(0, '{')
    result = '\n'.join(result)
    return result


def format_unchanged(arg, indent, result):
    """
    Формат вершины типа 'unchanged'
    """
    arg_str = format_arg(arg[2])
    elem = f'{BLANK_STR * indent}{DIFF_TYPE[arg[0]]}{arg[1]}: {arg_str}'
    result.append(elem)


def format_added(arg, indent, result):
    """
    Формат вершины типа 'added'
    """
    arg_str = arg[3]
    if isinstance(arg_str, dict):
        arg_str = format_complex_leaf(arg_str, indent + 1)
    else:
        arg_str = format_arg(arg[3])
    elem = f'{BLANK_STR * indent}{DIFF_TYPE["added"]}{arg[1]}: {arg_str}'
    result.append(elem)


def format_removed(arg, indent, result):
    """
    Формат вершины типа 'removed'
    """
    arg_str = arg[2]
    if isinstance(arg_str, dict):
        arg_str = format_complex_leaf(arg_str, indent + 1)
    else:
        arg_str = format_arg(arg_str)
    elem = f'{BLANK_STR * indent}{DIFF_TYPE["removed"]}{arg[1]}: {arg_str}'
    result.append(elem)


def format_changed(arg, indent, result):
    """
    Формат вершины типа 'changed'
    """
    format_removed(arg, indent, result)
    format_added(arg, indent, result)


def format_nested(arg, indent, result):
    """
    Формат вершины типа 'nested'
    """
    arg_str = get_stylish(arg[2], indent + 1)
    elem = f'{BLANK_STR * indent}{DIFF_TYPE[arg[0]]}{arg[1]}: {arg_str}'
    result.append(elem)


def format_complex_leaf(arg_dict, indent):
    """
    Обработка вложенного дерева
    """
    if not isinstance(arg_dict, dict):
        return format_arg(arg_dict)
    result = []
    for key, arg in arg_dict.items():
        start_str = BLANK_STR * (indent + 1)
        arg_str = format_complex_leaf(arg, indent + 1)
        result.append(f'{start_str}{key}: {arg_str}')
    result.append(f'{BLANK_STR * indent}}}')
    result.insert(0, '{')
    result = '\n'.join(result)
    return result