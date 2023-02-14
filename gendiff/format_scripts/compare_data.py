from gendiff.format_scripts.format_plain import get_plain
from gendiff.format_scripts.format_stylish import get_stylish
from gendiff.format_scripts.format_json import get_json
from gendiff.parse_data import parse


def get_diff_for_key(dict1, dict2, key):
    """
    Сравнивает значения двух словарей
    dict1 и dict2 по ключу key, возвращает
    кортеж с результатом сравнения
    """
    old_data = dict1.get(key, None)
    new_data = dict2.get(key, None)
    if old_data == new_data:
        result = ('unchanged', key, old_data, new_data)
    elif key not in dict1:
        result = ('added', key, old_data, new_data)
    elif key not in dict2:
        result = ('removed', key, old_data, new_data)
    elif isinstance(old_data, dict) and isinstance(new_data, dict):
        result = ('nested', key, get_diff_list(old_data, new_data), None)
    else:
        result = ('changed', key, old_data, new_data)
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


def get_diff_str(file_path1, file_path2, format):
    """
    Возвращает текстовый результат сравнения данных,
    в формате format, путь к файлам в
    переменных file_path1, file_path2
    """
    file1_ext = file_path1[-4:].upper()
    file2_ext = file_path1[-4:].upper()
    yaml_ext = ('.YML', 'YAML')
    if file1_ext == 'JSON' and file2_ext == 'JSON':
        data_type = 'JSON'
    elif file1_ext in yaml_ext and file2_ext in yaml_ext:
        data_type = 'YAML'
    else:
        return 'Unsupported file format!'
    parsed_data1 = parse(open(file_path1), data_type)
    parsed_data2 = parse(open(file_path2), data_type)
    diff_list = get_diff_list(parsed_data1, parsed_data2)
    result = ''
    if format == 'stylish':
        result = get_stylish(diff_list)
    elif format == 'plain':
        result = get_plain(diff_list)
    elif format == 'json':
        result = get_json(diff_list)
    return result
