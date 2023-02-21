

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
