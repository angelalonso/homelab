import pytest

import cli 
TESTFOLDER = './testfiles'

class TestAll:
    @classmethod
    def setup_class(cls):
        pass

    def test_loadObjectsStruct(self):
        file_objects = TESTFOLDER + "/objects_nofile.yaml"
        expected = None
        loaded_objects = cli.loadObjectsStruct(file_objects)
        assert loaded_objects == expected

        file_correct = TESTFOLDER + "/objects_correct.yaml"
        expected = {'gateways': ['name', 'mac_address'], 'hosts': ['name', 'mac_address']}
        loaded_objects = cli.loadObjectsStruct(file_correct)
        assert loaded_objects == expected

        pass

    # parse params
    # verb
    # objects-regex
    # object-full
    # objetct-key:value
