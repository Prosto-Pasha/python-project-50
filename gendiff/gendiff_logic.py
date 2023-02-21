from gendiff.formatters.format_plain import get_plain
from gendiff.formatters.format_stylish import get_stylish
from gendiff.formatters.format_json import get_json
from gendiff.parse_data import parse
from gendiff.compare_data import get_diff_list
from pathlib import Path
import argparse


GET_FORMAT = {
    'stylish': get_stylish,
    'plain': get_plain,
    'json': get_json
}


def parseargs(args):
    """
    Возвращает аргументы, указанные при запуске
    """
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file", type=str)
    parser.add_argument("second_file", type=str)
    # 'plain' or 'json'
    parser.add_argument(
        "-f", "--format",
        help="set format of output",
        type=str,
        default='stylish',
        choices=['stylish', 'plain', 'json']
    )
    return parser.parse_args(args)


def generate_diff(file_path1, file_path2, format='stylish'):
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
    with Path(file_path1).open() as file1:
        parsed_data1 = parse(file1, data_type)
    with Path(file_path2).open() as file2:
        parsed_data2 = parse(file2, data_type)
    diff_list = get_diff_list(parsed_data1, parsed_data2)
    return GET_FORMAT[format](diff_list)
