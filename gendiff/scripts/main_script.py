from gendiff.gendiff_logic import generate_diff, parseargs
import sys


def generate_diff_cli():
    """
    Сравнивает два файла и выводит результат сравнения
    """
    options = parseargs(sys.argv[1:])
    args = vars(options).values()
    print(generate_diff(*args))


def main():
    generate_diff_cli()


if __name__ == '__main__':
    main()
