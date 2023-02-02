import json
import yaml


BLANK_STR = '    '
PLUS_STR = '  + '
MINUS_STR = '  - '


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
    is_bool = isinstance(arg, bool)
    if arg is None:
        result = 'null'
    elif is_bool:
        result = bool_to_str(arg)
    else:
        result = str(arg)
    return result


def get_diff_for_key(dict1, dict2, key):
    '''
    Сравнивает значения двух словарей
    dict1 и dict2 по ключу key, возвращает
    список кортежей с результатом сравнения
    '''
    arg1 = get_item(dict1, key)
    arg2 = get_item(dict2, key)
    if arg1 == arg2:
        result = [(BLANK_STR, key, arg1)]
    elif arg1 is None:
        result = [(PLUS_STR, key, arg2)]
    elif arg2 is None:
        result = [(MINUS_STR, key, arg1)]
    elif isinstance(arg1, dict) and isinstance(arg2, dict):
        result = [(BLANK_STR, key, get_diff_list(arg1, arg2))]
    else:
        result = [(MINUS_STR, key, arg1),
                  (PLUS_STR, key, arg2)]
    return result


def get_diff_list(dict1, dict2):
    """
    Возвращает список с результом сравнения двух словарей
    """
    result = []
    keys1 = list(dict1.keys())
    keys2 = list(dict2.keys())
    all_keys = sorted(set(keys1 + keys2))
    for key in all_keys:
        result += get_diff_for_key(
            dict1,
            dict2,
            key
        )
    return result


def get_diff_string(diff_l, indent=0):
    """
    Возвращает строковое представление
    по списку различий двух словарей
    """
    result = []
    is_list = isinstance(diff_l, list)
    is_dict = isinstance(diff_l, dict)
    if not is_list and not is_dict:
        return str(diff_l)
    result.append('{')
    if is_dict:
        for key, arg in diff_l.items():
            start_str = BLANK_STR * (indent + 1)
            arg_str = get_diff_string(arg, indent + 1)
            result.append(f'{start_str}{key}: {arg_str}')
    indent_str = BLANK_STR * indent
    if is_list:
        for arg in diff_l:
            start_str = arg[0]
            key_str = arg[1]
            arg_str = get_diff_string(arg[2], indent + 1)
            result.append(f'{indent_str}{start_str}{key_str}: {arg_str}')
    result.append(f'{indent_str}}}')
    result = '\n'.join(result)
    return result


def compare_dict(dict1, dict2, format):
    """
    Возвращает строку с результатом сравнения двух словарей.
    """
    diff_list = get_diff_list(dict1, dict2)
    if format == 'stylish':
        return get_diff_string(diff_list)
    return diff_list


def compare_json(file_path1, file_path2, format):
    """
    Возвращает результат сравнения двух json-файлов
    """
    return compare_dict(
        json.load(open(file_path1)),
        json.load(open(file_path2)),
        format
    )


def compare_yaml(file_path1, file_path2, format):
    """
    Возвращает результат сравнения двух yaml-файлов
    """
    return compare_dict(
        yaml.safe_load(open(file_path1)),
        yaml.safe_load(open(file_path2)),
        format
    )
