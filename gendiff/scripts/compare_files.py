import json
import yaml


BLANK_STR = '    '
PLUS_STR = '  + '
MINUS_STR = '  - '


def get_item(arg_d, key):
    if key not in arg_d:
        return None
    arg = arg_d[key]
    if arg is None:
        return 'none'
    is_bool = isinstance(arg, bool)
    if is_bool and arg:
        return 'true'
    if is_bool and not arg:
        return 'false'
    if isinstance(arg, dict):
        return arg
    return str(arg)


def get_diff_for_key(dict1, dict2, key):
    '''
    Сравнивает значения двух словарей
    dict1 и dict2 по ключу key, возвращает
    список кортежей с результатом сравнения
    '''
    arg1 = get_item(dict1, key)
    arg2 = get_item(dict2, key)
    if arg1 == arg2:
        return [(BLANK_STR, key, arg1)]
    if arg1 is None:
        return [(PLUS_STR, key, arg2)]
    if arg2 is None:
        return [(MINUS_STR, key, arg1)]
    # Оба значения есть и они не равны
    if isinstance(arg1, dict) and isinstance(arg2, dict):
        return [(BLANK_STR, key, get_diff_list(arg1, arg2))]
    return [(MINUS_STR, key, arg1),
            (PLUS_STR, key, arg2)]


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