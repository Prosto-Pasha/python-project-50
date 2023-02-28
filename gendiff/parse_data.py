import json
import yaml
from pathlib import Path


def parse(file_path, data_type):
    """
    Возвращает данные из файла.
    file_path - путь к файлу
    data_type - тип данных
    """
    with Path(file_path).open() as file:
        if data_type == 'JSON':
            return json.load(file)
        elif data_type == 'YAML':
            return yaml.safe_load(file)
        else:
            raise Exception('Unsupported file format!')
