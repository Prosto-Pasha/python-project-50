from gendiff.format_scripts.format_plain import get_plain
from gendiff.format_scripts.format_stylish import get_stylish
from gendiff.format_scripts.format_json import get_json
from gendiff.format_scripts.parse_data import parse
from gendiff.format_scripts.format_common import get_item


def get_diff_for_key(dict1, dict2, key):
    """
    Сравнивает значения двух словарей
    dict1 и dict2 по ключу key, возвращает
    список кортеж с результатом сравнения
    """
    arg1 = get_item(dict1, key)
    arg2 = get_item(dict2, key)
    if arg1 == arg2:
        result = ('unchanged', key, arg1, arg2)
    elif arg1 is None:
        result = ('added', key, arg1, arg2)
    elif arg2 is None:
        result = ('removed', key, arg1, arg2)
    elif isinstance(arg1, dict) and isinstance(arg2, dict):
        result = ('nested', key, get_diff_list(arg1, arg2), None)
    else:
        result = ('changed', key, arg1, arg2)
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
        result.append(get_diff_for_key(dict1, dict2, key))
    return result


def compare_dict(dict1, dict2, format):
    """
    Возвращает строку с результатом сравнения двух словарей.
    """
    diff_list = get_diff_list(dict1, dict2)
    result = ''
    if format == 'stylish':
        result = get_stylish(diff_list)
    elif format == 'plain':
        result = get_plain(diff_list)
    elif format == 'json':
        result = get_json(diff_list)
    return result


def compare_data(data1, data2, format, data_type):
    """
    Возвращает текстовый результат сравнения данных
    """
    parsed_data1 = parse(data1, data_type)
    parsed_data2 = parse(data2, data_type)
    return compare_dict(parsed_data1, parsed_data2, format)
