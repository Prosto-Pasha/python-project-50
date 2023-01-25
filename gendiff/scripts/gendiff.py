import argparse
import json
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
        default='plain',
        # choices=['plain', 'json']
    )
    return parser.parse_args(args)


def get_diff_for_key(dict1, dict2, key):
    '''
    Сравнивает значения двух словарей
    dict1 и dict2 по ключу key,
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


def generate_diff(file_path1, file_path2, format='plain'):
    '''
    Получает пути к двум json-файлам,
    возвращает строку с результатом сравнения файлов
    '''
    dict1 = json.load(open(file_path1))
    dict2 = json.load(open(file_path2))
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
    result_list = list(map(lambda x: f'{x[0]} {x[1]}: {x[2]}', result_list))
    result = '{\n  ' + '\n  '.join(result_list) + '\n}'
    return result


def main():
    generate_diff_cli()


if __name__ == '__main__':
    main()
