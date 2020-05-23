import api
import unittest

TESTFOLDER = './testfiles'


class TestAll(unittest.TestCase):
    def test_loadObjectStruct(self):
        file_nonexist = TESTFOLDER + "/objects_nofile.yaml"
        expected = None
        loaded_objects = api.loadObjectStruct(file_nonexist)
        assert loaded_objects == expected

        file_correct = TESTFOLDER + "/objects_correct.yaml"
        expected = {'gateway': ['name', 'mac_address'],
                    'host': ['name', 'mac_address']}
        loaded_objects = api.loadObjectStruct(file_correct)
        assert loaded_objects == expected
