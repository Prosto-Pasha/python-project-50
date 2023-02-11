
def bool_to_str(arg):
    """
    Преобразует булево к строке
    """
    return 'true' if arg else 'false'


def get_item(arg_d, key):
    """
    Возвращает преобразованное значение
    словаря arg_d по ключу key
    """
    if key not in arg_d:
        return None
    arg = arg_d[key]
    if isinstance(arg, dict):
        return arg
    if arg is None:
        result = 'null'
    elif isinstance(arg, bool):
        result = bool_to_str(arg)
    else:
        result = arg
    return result
