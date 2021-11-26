import pytest
import os.path
import server.FileService as FileService


@pytest.fixture(scope='function')
def create_file():
    with open('example_delete.py', mode='w', encoding='utf-8') as f:
        f.write("hello from test")
    yield


def test_exception_1():
    with pytest.raises(FileService.ElementNotExistError):
        FileService.delete_file('NNNexample_delete.py')


def test_exception_3(create_file):
    FileService.delete_file('example_delete.py')
    assert not os.path.isfile('example_delete.py')