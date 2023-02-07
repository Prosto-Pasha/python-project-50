import json
import yaml


def parse(data, data_type):
    """
    Возвращает преобразованные данные
    (словарь) для указанного формата
    """
    if data_type == 'JSON':
        return json.load(data)
    else:
        return yaml.safe_load(data)
