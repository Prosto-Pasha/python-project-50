
def format_arg(arg):
    """
    Возвращает форматированное значение аргумента
    """
    if arg is None:
        return 'null'
    if isinstance(arg, bool):
        return 'true' if arg else 'false'
    return str(arg)
