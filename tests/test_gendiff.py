import pytest
from gendiff.scripts.gendiff import generate_diff, parseargs


@pytest.fixture
def file1_json():
    return 'tests/fixtures/file1.json'


@pytest.fixture
def file2_json():
    return 'tests/fixtures/file2.json'


@pytest.fixture
def file3_json():
    return 'tests/fixtures/file3.json'


@pytest.fixture
def file4_json():
    return 'tests/fixtures/file4.json'


@pytest.fixture
def file1_yml():
    return 'tests/fixtures/file1.yml'


@pytest.fixture
def file2_yml():
    return 'tests/fixtures/file2.yml'


@pytest.fixture
def file3_yml():
    return 'tests/fixtures/file3.yaml'


@pytest.fixture
def file4_yml():
    return 'tests/fixtures/file4.yaml'


@pytest.fixture
def correct_result1():
    """
    Результат сравнения файлов 1 и 2
    (json и yaml) в формате stylish
    """
    return open('tests/fixtures/correct_result1.txt').read()


@pytest.fixture
def correct_result2():
    """
    Результат сравнения файлов 3 и 4
    (json и yaml) в формате stylish
    """
    start_text = open('tests/fixtures/correct_result2.txt').read()
    end_text = open('tests/fixtures/correct_result2_end.txt').read()
    return f'{start_text} {end_text}'


@pytest.fixture
def correct_result3():
    """
    Результат сравнения файлов 1 и 2
    (json и yaml) в формате plain
    """
    return open('tests/fixtures/correct_result3.txt').read()


@pytest.fixture
def correct_result4():
    """
    Результат сравнения файлов 3 и 4
    (json и yaml) в формате plain
    """
    return open('tests/fixtures/correct_result4.txt').read()


@pytest.fixture
def correct_result5():
    """
    Результат сравнения файлов 1 и 2
    (json и yaml) в формате json
    """
    return open('tests/fixtures/correct_result5.txt').read()


@pytest.fixture
def correct_result6():
    """
    Результат сравнения файлов 3 и 4
    (json и yaml) в формате json
    """
    return open('tests/fixtures/correct_result6.txt').read()


@pytest.mark.parametrize("file1,file2,correct_result,format", [
    ('file1_json', 'file2_json', 'correct_result1', 'stylish'),
    ('file3_json', 'file4_json', 'correct_result2', 'stylish'),
    ('file1_json', 'file2_json', 'correct_result3', 'plain'),
    ('file3_json', 'file4_json', 'correct_result4', 'plain'),
    ('file1_json', 'file2_json', 'correct_result5', 'json'),
    ('file3_json', 'file4_json', 'correct_result6', 'json'),
    ('file1_yml', 'file2_yml', 'correct_result1', None),
    ('file3_yml', 'file4_yml', 'correct_result2', 'stylish'),
    ('file1_yml', 'file2_yml', 'correct_result3', 'plain'),
    ('file3_yml', 'file4_yml', 'correct_result4', 'plain'),
    ('file1_yml', 'file2_yml', 'correct_result5', 'json'),
    ('file3_yml', 'file4_yml', 'correct_result6', 'json'),
])
def test_eval(file1, file2, correct_result, format, request):
    """
    Тесты функции generate_diff
    с тестовыми файлами JSON и YAML
    с выводом результата в разных форматах
    """
    file1 = request.getfixturevalue(file1)
    file2 = request.getfixturevalue(file2)
    correct_result = request.getfixturevalue(correct_result)
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
    result = generate_diff('some_file1.txt', 'some_file2.txt')
    assert result == 'Unsupported files!'


def test_parser():
    parser = parseargs(['file1.json', 'file2.json'])
    assert parser.first_file == 'file1.json'
    assert parser.second_file == 'file2.json'
