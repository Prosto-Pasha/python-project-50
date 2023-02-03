from gendiff.scripts.compare_files import compare_files
import argparse
import sys


def generate_diff_cli():
    '''
    Сравнивает два файла и выводит результат сравнения
    '''
    options = parseargs(sys.argv[1:])
    args = vars(options).values()
    print(generate_diff(*args))


def parseargs(args):
    '''
    Возвращает аргументы, указанные при запуске
    '''
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
        # choices=['plain', 'json']
    )
    return parser.parse_args(args)


def generate_diff(file_path1, file_path2, format='stylish'):
    '''
    Получает пути к двум файлам,
    возвращает строку с результатом сравнения файлов
    '''
    file1_ext = file_path1[-4:].upper()
    file2_ext = file_path1[-4:].upper()
    yaml_ext = ('.YML', 'YAML')
    if file1_ext == 'JSON' and file2_ext == 'JSON':
        file_type = 'JSON'
    elif file1_ext in yaml_ext and file2_ext in yaml_ext:
        file_type = 'YAML'
    else:
        return 'Unsupported files!'
    return compare_files(file_path1, file_path2, format, file_type)


def main():
    generate_diff_cli()


if __name__ == '__main__':
    main()
