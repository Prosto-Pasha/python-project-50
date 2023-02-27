from gendiff.formatters.format_common import format_arg


DIFF_TO_STR = {
    'added': '  + ',
    'removed': '  - ',
    'unchanged': '    ',
    'nested': '    ',
    'changed': ' -+ ',
}
BLANK_STR = '    '
TYPE = 0
KEY = 1
OLD_VALUE = 2
NEW_VALUE = 3


def get_stylish(diff, depth=0):
    """
    Возвращает строковое представление
    по списку различий двух словарей
    в формате stylish
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
        format_vertex(vertex, depth, result)
    result.append(f'{BLANK_STR * depth}}}')
    result.insert(0, '{')
    result = '\n'.join(result)
    return result


def format_unchanged(vertex, depth, result):
    """
    Формат вершины типа 'unchanged'
    """
    vertex_to_str = (f'{BLANK_STR * depth}'
                     f'{DIFF_TO_STR[vertex[TYPE]]}'
                     f'{vertex[KEY]}: '
                     f'{format_arg(vertex[OLD_VALUE])}')
    result.append(vertex_to_str)


def format_added(vertex, depth, result):
    """
    Формат вершины типа 'added'
    """
    if isinstance(vertex[NEW_VALUE], dict):
        value_to_str = format_complex_leaf(
            vertex[NEW_VALUE],
            depth + 1
        )
    else:
        value_to_str = format_arg(vertex[NEW_VALUE])
    vertex_to_str = (f'{BLANK_STR * depth}'
                     f'{DIFF_TO_STR["added"]}'
                     f'{vertex[KEY]}: '
                     f'{value_to_str}')
    result.append(vertex_to_str)


def format_removed(vertex, depth, result):
    """
    Формат вершины типа 'removed'
    """
    if isinstance(vertex[OLD_VALUE], dict):
        value_to_str = format_complex_leaf(
            vertex[OLD_VALUE],
            depth + 1
        )
    else:
        value_to_str = format_arg(vertex[OLD_VALUE])
    vertex_to_str = (f'{BLANK_STR * depth}'
                     f'{DIFF_TO_STR["removed"]}'
                     f'{vertex[KEY]}: '
                     f'{value_to_str}')
    result.append(vertex_to_str)


def format_changed(arg, depth, result):
    """
    Формат вершины типа 'changed'
    """
    format_removed(arg, depth, result)
    format_added(arg, depth, result)


def format_nested(vertex, depth, result):
    """
    Формат вершины типа 'nested'
    """
    value_to_str = get_stylish(
        vertex[OLD_VALUE],
        depth + 1
    )
    vertex_to_str = (f'{BLANK_STR * depth}'
                     f'{DIFF_TO_STR[vertex[TYPE]]}'
                     f'{vertex[KEY]}: '
                     f'{value_to_str}')
    result.append(vertex_to_str)


def format_complex_leaf(vertex, depth):
    """
    Обработка вложенного дерева
    """
    if not isinstance(vertex, dict):
        return format_arg(vertex)
    result = []
    for key, arg in vertex.items():
        vertex_to_str = (f'{BLANK_STR * (depth + 1)}'
                         f'{key}: '
                         f'{format_complex_leaf(arg, depth + 1)}')
        result.append(vertex_to_str)
    result.append(f'{BLANK_STR * depth}}}')
    result.insert(0, '{')
    result = '\n'.join(result)
    return result
