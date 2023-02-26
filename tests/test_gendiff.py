import pytest
from pathlib import Path
from gendiff.gendiff_logic import generate_diff, parseargs


def get_data_from_file(file_name):
    """
    Возвращает данные из файла, расположенного
    в папке fixtures по имени файла
    """
    with Path(get_full_file_name(file_name)).open() as file:
        result = file.read()
    return result


def get_full_file_name(file_name):
    """
    Возвращает путь к файлу в папке fixtures
    по имени файла
    """
    return f'tests/fixtures/{file_name}'


def get_data(file_name):
    """
    Возвращает данные из файла/ов
    """
    if isinstance(file_name, tuple):
        start_data = get_data_from_file(file_name[0])
        end_data = get_data_from_file(file_name[1])
        result = ' '.join((start_data, end_data))
    else:
        result = get_data_from_file(file_name)
    return result


@pytest.mark.parametrize("file1,file2,correct_result,format", [
    ('file1.json', 'file2.json', 'correct_result1.txt', 'stylish'),
    ('file3.json', 'file4.json', (
        'correct_result2.txt',
        'correct_result2_end.txt'
    ), 'stylish'),
    ('file1.json', 'file2.json', 'correct_result3.txt', 'plain'),
    ('file3.json', 'file4.json', 'correct_result4.txt', 'plain'),
    ('file1.json', 'file2.json', 'correct_result5.txt', 'json'),
    ('file3.json', 'file4.json', 'correct_result6.txt', 'json'),
    ('file1.yml', 'file2.yml', 'correct_result1.txt', None),
    ('file3.yaml', 'file4.yaml', (
        'correct_result2.txt',
        'correct_result2_end.txt'
    ), 'stylish'),
    ('file1.yml', 'file2.yml', 'correct_result3.txt', 'plain'),
    ('file3.yaml', 'file4.yaml', 'correct_result4.txt', 'plain'),
    ('file1.yml', 'file2.yml', 'correct_result5.txt', 'json'),
    ('file3.yaml', 'file4.yaml', 'correct_result6.txt', 'json'),
])
def test_eval(file1, file2, correct_result, format):
    """
    Тесты функции generate_diff
    с тестовыми файлами JSON и YAML
    с выводом результата в разных форматах
    """
    file1 = get_full_file_name(file1)
    file2 = get_full_file_name(file2)
    correct_result = get_data(correct_result)
    if format is None:
        result = generate_diff(file1, file2)
    else:
        result = generate_diff(file1, file2, format)
    assert result == correct_result


def test_unsupported_files():
    """
    Тест функции generate_diff
    с неподдерживаемыми файлами
    формат по умолчанию
    """
    with pytest.raises(Exception) as e:
        result = generate_diff('some_file1.txt', 'some_file2.txt')
    assert str(e.value) == 'Unsupported file format!'


def test_parser():
    parser = parseargs(['file1.json', 'file2.json'])
    assert parser.first_file == 'file1.json'
    assert parser.second_file == 'file2.json'
