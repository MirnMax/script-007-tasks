import pytest
import server.FileService as FileService

filename = 'example.py'
class TestVelues:
    def test_get_files(self):
        check_list = ['name', 'create_date', 'edit_date', 'size']
        first_dict = FileService.get_files()[0]
        list_keys = [x for x in first_dict.keys()]
        assert check_list == list_keys

    def test_get_file_data(self):
        check_list = ['name', 'create_date', 'edit_date', 'size', 'context']
        first_dict = FileService.get_file_data(filename)
        list_keys = [x for x in first_dict.keys()]
        assert check_list == list_keys


