from gendiff.formatters.format_common import format_arg


TYPE = 0
KEY = 1
OLD_VALUE = 2
NEW_VALUE = 3


def get_plain(diff, path=''):
    """
    Возвращает строковое представление по списку
    различий двух словарей в формате plain
    """
    format_vertex_vars = {
        'unchanged': format_unchanged,
        'added': format_added,
        'removed': format_removed,
        'nested': format_nested,
        'changed': format_changed}
    result = []
    for vertex in diff:
        format_vertex = format_vertex_vars[vertex[TYPE]]
        formatted_vertex = format_vertex(vertex, path)
        if formatted_vertex is not None:
            result.append(formatted_vertex)
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
    return (f"Property '{get_path(path, arg[KEY])}' "
            f"was added with value: {stringify_value(arg[NEW_VALUE])}")


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
    return get_plain(arg[OLD_VALUE], get_path(path, arg[KEY]))


def format_changed(arg, path):
    """
    Формат вершины типа 'changed'
    """
    return (f"Property '{get_path(path, arg[KEY])}' "
            f"was updated. From {stringify_value(arg[OLD_VALUE])} "
            f"to {stringify_value(arg[NEW_VALUE])}")


def stringify_value(arg):
    """
    Возвращает текстовое представление значения
    аргумента arg в формате plain
    """
    if isinstance(arg, dict):
        return '[complex value]'
    if isinstance(arg, int) or isinstance(arg, bool) or arg is None:
        return format_arg(arg)
    return f"'{arg}'"
