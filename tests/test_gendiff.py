import pytest
from gendiff.scripts.gendiff import generate_diff, parseargs


@pytest.fixture
def get_file1_json():
    return 'tests/fixtures/file1.json'


@pytest.fixture
def get_file2_json():
    return 'tests/fixtures/file2.json'


@pytest.fixture
def get_file1_yml():
    return 'tests/fixtures/file1.yml'


@pytest.fixture
def get_file2_yml():
    return 'tests/fixtures/file2.yml'


@pytest.fixture
def correct_result():
    return '''{
  - follow: False
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: True
}'''


def test_generate_diff_json(
        get_file1_json,
        get_file2_json,
        correct_result
):
    '''
    Тест функции generate_diff с тестовыми файлами JSON
    '''
    format = 'plain'
    result = generate_diff(get_file1_json, get_file2_json, format)
    assert result == correct_result


def test_generate_diff_yml(
        get_file1_yml,
        get_file2_yml,
        correct_result
):
    '''
    Тест функции generate_diff с тестовыми файлами YML, YAML
    '''
    format = 'plain'
    result = generate_diff(get_file1_yml, get_file2_yml, format)
    assert result == correct_result


def test_parser():
    parser = parseargs(['file1.json', 'file2.json'])
    assert parser.first_file == 'file1.json'
    assert parser.second_file == 'file2.json'
