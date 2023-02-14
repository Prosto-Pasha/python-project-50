import json
import yaml


def parse(data, data_type):
    """
    Возвращает преобразованные данные
    (словарь) для указанного формата
    """
    if data_type == 'JSON':
        return json.load(data)
    elif data_type == 'YAML':
        return yaml.safe_load(data)
    else:
        raise Exception('Unsupported file format!')
