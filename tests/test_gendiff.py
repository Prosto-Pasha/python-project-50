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
    """
    Результат сравнения файлов 1 и 2
    (json и yaml) в формате stylish
    """
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
    """
    Результат сравнения файлов 3 и 4
    (json и yaml) в формате stylish
    """
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


@pytest.fixture
def correct_result3():
    """
    Результат сравнения файлов 1 и 2
    (json и yaml) в формате plain
    """
    return '''Property 'follow' was removed
Property 'proxy' was removed
Property 'timeout' was updated. From 50 to 20
Property 'verbose' was added with value: true'''


@pytest.fixture
def correct_result4():
    """
    Результат сравнения файлов 3 и 4
    (json и yaml) в формате plain
    """
    return '''Property 'common.follow' was added with value: false
Property 'common.setting2' was removed
Property 'common.setting3' was updated. From true to null
Property 'common.setting4' was added with value: 'blah blah'
Property 'common.setting5' was added with value: [complex value]
Property 'common.setting6.doge.wow' was updated. From '' to 'so much'
Property 'common.setting6.ops' was added with value: 'vops'
Property 'group1.baz' was updated. From 'bas' to 'bars'
Property 'group1.nest' was updated. From [complex value] to 'str'
Property 'group2' was removed
Property 'group3' was added with value: [complex value]'''


def test_generate_diff_json(
        get_file1_json,
        get_file2_json,
        correct_result1
):
    '''
    Тест функции generate_diff
    с тестовыми файлами JSON 1 и 2
    формат stylish
    '''
    format = 'stylish'
    result = generate_diff(get_file1_json, get_file2_json, format)
    assert result == correct_result1


def test_2_generate_diff_json(
        get_file3_json,
        get_file4_json,
        correct_result2
):
    """
    Тест 2 функции generate_diff
    с тестовыми файлами JSON 3 и 4
    формат stylish
    """
    format = 'stylish'
    result = generate_diff(get_file3_json, get_file4_json, format)
    assert result == correct_result2


def test_3_generate_diff_json(
        get_file1_json,
        get_file2_json,
        correct_result3
):
    """
    Тест 3 функции generate_diff
    с тестовыми файлами JSON 1 и 2
    формат plain
    """
    format = 'plain'
    result = generate_diff(get_file1_json, get_file2_json, format)
    assert result == correct_result3


def test_4_generate_diff_json(
        get_file3_json,
        get_file4_json,
        correct_result4
):
    """
    Тест 4 функции generate_diff
    с тестовыми файлами JSON 3 и 4
    формат plain
    """
    format = 'plain'
    result = generate_diff(get_file3_json, get_file4_json, format)
    assert result == correct_result4


def test_generate_diff_yml(
        get_file1_yml,
        get_file2_yml,
        correct_result1
):
    """
    Тест 1 функции generate_diff
    с тестовыми файлами YML, YAML 1 и 2
    default формат (stylish)
    """
    # default format
    result = generate_diff(get_file1_yml, get_file2_yml)
    assert result == correct_result1


def test_2_generate_diff_yml(
        get_file3_yml,
        get_file4_yml,
        correct_result2
):
    """
    Тест 2 функции generate_diff
    с тестовыми файлами YML, YAML 3 и 4
    формат stylish
    """
    format = 'stylish'
    result = generate_diff(get_file3_yml, get_file4_yml, format)
    assert result == correct_result2


def test_3_generate_diff_yml(
        get_file1_yml,
        get_file2_yml,
        correct_result3
):
    """
    Тест 3 функции generate_diff
    с тестовыми файлами YML, YAML 1 и 2
    формат plain
    """
    format = 'plain'
    result = generate_diff(get_file1_yml, get_file2_yml, format)
    assert result == correct_result3


def test_4_generate_diff_yml(
        get_file3_yml,
        get_file4_yml,
        correct_result4
):
    """
    Тест 4 функции generate_diff
    с тестовыми файлами YML, YAML 3 и 4
    формат plain
    """
    format = 'plain'
    result = generate_diff(get_file3_yml, get_file4_yml, format)
    assert result == correct_result4


def test_parser():
    parser = parseargs(['file1.json', 'file2.json'])
    assert parser.first_file == 'file1.json'
    assert parser.second_file == 'file2.json'
