import pytest
import os.path
import server.FileService as FileService

filename = 'exam.py'

class TestFunctions:

    def test_create_file(self):
        if os.path.isfile(filename):
            FileService.delete_file(filename)
        FileService.create_file(filename)
        assert os.path.isfile(filename)

    def test_delete_file(self):
        if not os.path.isfile(filename):
            FileService.create_file(filename)
        FileService.delete_file(filename)
        assert not os.path.isfile(filename)



