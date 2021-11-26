import pytest
import server.FileService as FileService

class TestExceptions:
    def test_exception_1(self):
        with pytest.raises(FileService.ElementNotExistError):
            FileService.get_file_data('exam.py')

    def test_exception_2(self):
        with pytest.raises(FileService.ElementNotExistError):
            FileService.delete_file('exam.py')
    def test_exception_3(self):
        with pytest.raises(FileService.ElementNotExistError):
            FileService.change_dir('exam.py', False)









