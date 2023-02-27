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
        formatted_vertex = format_vertex(vertex, depth)
        result.append(formatted_vertex)
    result = ['{'] + result + [f'{BLANK_STR * depth}}}']
    return '\n'.join(result)


def format_unchanged(vertex, depth):
    """
    Формат вершины типа 'unchanged'
    """
    return (f'{BLANK_STR * depth}'
            f'{DIFF_TO_STR[vertex[TYPE]]}'
            f'{vertex[KEY]}: '
            f'{format_arg(vertex[OLD_VALUE])}')


def format_added(vertex, depth):
    """
    Формат вершины типа 'added'
    """
    return (f'{BLANK_STR * depth}'
            f'{DIFF_TO_STR["added"]}'
            f'{vertex[KEY]}: '
            f'{stringify_value(vertex[NEW_VALUE], depth)}')


def format_removed(vertex, depth):
    """
    Формат вершины типа 'removed'
    """
    return (f'{BLANK_STR * depth}'
            f'{DIFF_TO_STR["removed"]}'
            f'{vertex[KEY]}: '
            f'{stringify_value(vertex[OLD_VALUE], depth)}')


def format_changed(vertex, depth):
    """
    Формат вершины типа 'changed'
    """
    return '\n'.join(
        [
            format_removed(vertex, depth),
            format_added(vertex, depth)
        ]
    )


def format_nested(vertex, depth):
    """
    Формат вершины типа 'nested'
    """
    return (f'{BLANK_STR * depth}'
            f'{DIFF_TO_STR[vertex[TYPE]]}'
            f'{vertex[KEY]}: '
            f'{get_stylish(vertex[OLD_VALUE], depth + 1)}')


def format_complex_leaf(vertex, depth):
    """
    Обработка вложенного дерева
    """
    if not isinstance(vertex, dict):
        return format_arg(vertex)
    result = []
    for key, value in vertex.items():
        vertex_to_str = (f'{BLANK_STR * (depth + 1)}'
                         f'{key}: '
                         f'{format_complex_leaf(value, depth + 1)}')
        result.append(vertex_to_str)
    result = ['{'] + result + [f'{BLANK_STR * depth}}}']
    return '\n'.join(result)


def stringify_value(vertex, depth):
    """
    Возвращает текстовое представление значения
    аргумента vertex в формате plain
    """
    if isinstance(vertex, dict):
        return format_complex_leaf(
            vertex,
            depth + 1
        )
    return format_arg(vertex)
