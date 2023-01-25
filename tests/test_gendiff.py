import pytest
from gendiff.scripts.gendiff import generate_diff


@pytest.fixture
def get_file1():
    return 'tests/fixtures/file1.json'


@pytest.fixture
def get_file2():
    return 'tests/fixtures/file2.json'


def test_generate_diff(get_file1, get_file2):
    '''
    Тест функции generate_diff с тестовыми файлами
    '''
    format = 'plain'
    correct_result = '''{
  - follow: False
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: True
}'''
    result = generate_diff(get_file1, get_file2, format)
    assert result == correct_result
