import json
import yaml


def get_diff_for_key(dict1, dict2, key):
    '''
    Сравнивает значения двух словарей
    dict1 и dict2 по ключу key, возвращает
    список кортежей с результатом сравнения
    '''
    arg1 = dict1.get(key)
    arg2 = dict2.get(key)
    if arg1 is None:
        return [('+', key, arg2),]
    if arg2 is None:
        return [('-', key, arg1),]
    if arg1 == arg2:
        return [(' ', key, arg1),]
    else:
        return [('-', key, arg1),
                ('+', key, arg2)]


def compare_dict(dict1, dict2):
    '''
    Возвращает строку с результом сравнения двух словарей
    '''
    keys1 = list(dict1.keys())
    keys2 = list(dict2.keys())
    all_keys = sorted(set(keys1 + keys2))
    result_list = []
    for key in all_keys:
        result_list += get_diff_for_key(
            dict1,
            dict2,
            key
        )
    result_list = list(map(
        lambda x: f'{x[0]} {x[1]}: {x[2]}',
        result_list)
    )
    result = '{\n  ' + '\n  '.join(result_list) + '\n}'
    return result


def compare_json(file_path1, file_path2, format):
    '''
    Возвращает результат сравнения двух json-файлов
    '''
    return compare_dict(
        json.load(open(file_path1)),
        json.load(open(file_path2))
    )


def compare_yaml(file_path1, file_path2, format):
    '''
    Возвращает результат сравнения двух json-файлов
    '''
    return compare_dict(
        yaml.safe_load(open(file_path1)),
        yaml.safe_load(open(file_path2))
    )
