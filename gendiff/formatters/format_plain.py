from gendiff.formatters.format_common import format_arg


TYPE = 0
KEY = 1
OLD_VALUE = 2
NEW_VALUE = 3


def get_plain(diff_l, path=''):
    """
    Возвращает строковое представление по списку
    различий двух словарей в формате plain
    """
    vertex_func = {
        'unchanged': format_unchanged,
        'added': format_added,
        'removed': format_removed,
        'nested': format_nested,
        'changed': format_changed}
    result = []
    for arg in diff_l:
        func = vertex_func[arg[TYPE]]
        list_item = func(arg, path)
        if list_item is not None:
            result.append(list_item)
    result = '\n'.join(result)
    return result


def get_path(path, branch):
    """
    Возвращает полный путь текущего значения
    """
    return f'{path}.{branch}' if path else branch


def format_unchanged(arg, path):
    """
    Формат вершины типа 'unchanged'
    """
    return None


def format_added(arg, path):
    """
    Формат вершины типа 'added'
    """
    value_str = get_value_str(arg[NEW_VALUE])
    path = get_path(path, arg[KEY])
    middle_text = 'was added with value:'
    return f"Property '{path}' {middle_text} {value_str}"


def format_removed(arg, path):
    """
    Формат вершины типа 'removed'
    """
    path = get_path(path, arg[KEY])
    return f"Property '{path}' was removed"


def format_nested(arg, path):
    """
    Формат вершины типа 'nested'
    """
    path = get_path(path, arg[KEY])
    return get_plain(arg[OLD_VALUE], path)


def format_changed(arg, path):
    """
    Формат вершины типа 'changed'
    """
    path = get_path(path, arg[KEY])
    middle_text = 'was updated. From'
    value_str_arg1 = get_value_str(arg[OLD_VALUE])
    value_str_arg2 = get_value_str(arg[NEW_VALUE])
    arg1_arg2_str = f'{middle_text} {value_str_arg1} to {value_str_arg2}'
    return f"Property '{path}' {arg1_arg2_str}"


def get_value_str(arg):
    """
    Возвращает текстовое представление значения
    аргумента arg в формате plain
    """
    if isinstance(arg, dict):
        return '[complex value]'
    if isinstance(arg, int) or isinstance(arg, bool) or arg is None:
        return format_arg(arg)
    return f"'{arg}'"
