from gendiff.scripts.format_diff import get_diff_string
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


def compare_dict(dict1, dict2, format):
    """
    Возвращает строку с результатом сравнения двух словарей.
    """
    diff_list = get_diff_list(dict1, dict2)
    return get_diff_string(diff_list, format)


def compare_files(file_path1, file_path2, format, file_type):
    """
    Возвращает результат сравнения двух json-файлов
    """
    if file_type == 'JSON':
        dict1 = json.load(open(file_path1))
        dict2 = json.load(open(file_path2))
    else:
        dict1 = yaml.safe_load(open(file_path1))
        dict2 = yaml.safe_load(open(file_path2))
    return compare_dict(dict1, dict2, format)
