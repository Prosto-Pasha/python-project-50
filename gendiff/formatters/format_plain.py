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


def format_unchanged(vertex, path):
    """
    Формат вершины типа 'unchanged'
    """
    return None


def format_added(vertex, path):
    """
    Формат вершины типа 'added'
    """
    return (f"Property '{get_path(path, vertex[KEY])}' "
            f"was added with value: {stringify_value(vertex[NEW_VALUE])}")


def format_removed(vertex, path):
    """
    Формат вершины типа 'removed'
    """
    path = get_path(path, vertex[KEY])
    return f"Property '{path}' was removed"


def format_nested(vertex, path):
    """
    Формат вершины типа 'nested'
    """
    return get_plain(vertex[OLD_VALUE], get_path(path, vertex[KEY]))


def format_changed(vertex, path):
    """
    Формат вершины типа 'changed'
    """
    return (f"Property '{get_path(path, vertex[KEY])}' "
            f"was updated. From {stringify_value(vertex[OLD_VALUE])} "
            f"to {stringify_value(vertex[NEW_VALUE])}")


def stringify_value(vertex):
    """
    Возвращает текстовое представление значения
    аргумента vertex в формате plain
    """
    if isinstance(vertex, dict):
        return '[complex value]'
    if any((
            isinstance(vertex, int),
            isinstance(vertex, bool),
            vertex is None
    )):
        return format_arg(vertex)
    return f"'{vertex}'"
