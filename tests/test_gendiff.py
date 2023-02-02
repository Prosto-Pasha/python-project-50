import pytest
from gendiff.scripts.gendiff import generate_diff, parseargs


@pytest.fixture
def get_file1_json():
    return 'tests/fixtures/file1.json'


@pytest.fixture
def get_file2_json():
    return 'tests/fixtures/file2.json'


@pytest.fixture
def get_file3_json():
    return 'tests/fixtures/file3.json'


@pytest.fixture
def get_file4_json():
    return 'tests/fixtures/file4.json'


@pytest.fixture
def get_file1_yml():
    return 'tests/fixtures/file1.yml'


@pytest.fixture
def get_file2_yml():
    return 'tests/fixtures/file2.yml'


@pytest.fixture
def get_file3_yml():
    return 'tests/fixtures/file3.yaml'


@pytest.fixture
def get_file4_yml():
    return 'tests/fixtures/file4.yaml'


@pytest.fixture
def correct_result1():
    return '''{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}'''


@pytest.fixture
def correct_result2():
    return '''{
    common: {
      + follow: false
        setting1: Value 1
      - setting2: 200
      - setting3: true
      + setting3: null
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
        setting6: {
            doge: {
              - wow: 
              + wow: so much
            }
            key: value
          + ops: vops
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
      - nest: {
            key: value
        }
      + nest: str
    }
  - group2: {
        abc: 12345
        deep: {
            id: 45
        }
    }
  + group3: {
        deep: {
            id: {
                number: 45
            }
        }
        fee: 100500
    }
}'''


def test_generate_diff_json(
        get_file1_json,
        get_file2_json,
        correct_result1
):
    '''
    Тест функции generate_diff с тестовыми файлами JSON
    '''
    format = 'stylish'
    result = generate_diff(get_file1_json, get_file2_json, format)
    assert result == correct_result1


def test_2_generate_diff_json(
        get_file3_json,
        get_file4_json,
        correct_result2
):
    '''
    Тест 2 функции generate_diff с тестовыми файлами JSON 3 и 4
    '''
    format = 'stylish'
    result = generate_diff(get_file3_json, get_file4_json, format)
    assert result == correct_result2


def test_generate_diff_yml(
        get_file1_yml,
        get_file2_yml,
        correct_result1
):
    '''
    Тест функции generate_diff с тестовыми файлами YML, YAML
    '''
    # default format
    result = generate_diff(get_file1_yml, get_file2_yml)
    assert result == correct_result1


def test2_generate_diff_yml(
        get_file3_yml,
        get_file4_yml,
        correct_result2
):
    '''
    Тест 2 функции generate_diff с тестовыми файлами YML, YAML 3 и 4
    '''
    format = 'stylish'
    result = generate_diff(get_file3_yml, get_file4_yml, format)
    assert result == correct_result2


def test_parser():
    parser = parseargs(['file1.json', 'file2.json'])
    assert parser.first_file == 'file1.json'
    assert parser.second_file == 'file2.json'
