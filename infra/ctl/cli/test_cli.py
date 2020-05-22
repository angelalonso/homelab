import cli
import os
from dotenv import load_dotenv
from unittest.mock import patch
import unittest

TESTFOLDER = './testfiles'


class TestAll(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        pass

    def test_loadObjectStruct(self):
        file_nonexist = TESTFOLDER + "/objects_nofile.yaml"
        expected = None
        loaded_objects = cli.loadObjectStruct(file_nonexist)
        assert loaded_objects == expected

        file_correct = TESTFOLDER + "/objects_correct.yaml"
        expected = {'gateway': ['name', 'mac_address'],
                    'host': ['name', 'mac_address']}
        loaded_objects = cli.loadObjectStruct(file_correct)
        assert loaded_objects == expected

    def test_loadVerbStruct(self):
        file_nonexist = TESTFOLDER + "/verbs_nofile.yaml"
        expected = None
        loaded_verbs = cli.loadVerbStruct(file_nonexist)
        assert loaded_verbs == expected

        file_correct = TESTFOLDER + "/verbs_correct.yaml"
        expected = {'get':
                    {'args':
                     {'arg_1': ['search_string', 'key_value']}},
                    'update':
                    {'args':
                     {'arg_1': ['search_string', 'key_value'],
                      'arg_2': ['object_full', 'key_value']}}}
        loaded_verbs = cli.loadVerbStruct(file_correct)
        assert loaded_verbs == expected

    def test_loadArgs(self):
        verbs = ['get', 'add']
        objects = {'gateway':
                   ['name', 'mac_address'],
                   'host':
                   ['name', 'mac_address']}
        verb, obj, params = cli.loadArgs(verbs,
                                         objects,
                                         'test_cli.py get host bla bla'.split())  # noqa E501

    def test_createObject(self):
        verb_struct = cli.loadVerbStruct(TESTFOLDER + "/verbs_correct.yaml")
        obj_struct = cli.loadObjectStruct(TESTFOLDER + "/objects_correct.yaml")
        # test search_string
        params_object = {'name': 'server1%', 'mac_address': None}
        param = 'server1%'
        assert cli.createObject(verb_struct,
                                obj_struct,
                                'host',
                                param) == params_object
        # test key_value
        params_object = {'name': None, 'mac_address': 'aa:bb:cc:dd:ee'}
        param = 'mac_address=aa:bb:cc:dd:ee'
        assert cli.createObject(verb_struct,
                                obj_struct,
                                'host',
                                param) == params_object
        # TODO: assert system exit 2
        # param = 'mac_addre=aa:bb:cc:dd:ee'
        # assert cli.checkParams(verb_struct,
        # obj_struct,
        # 'host',
        # param) == params_object
        params_object = {'name': 'test1', 'mac_address': 'aa:bb:cc:dd:ee'}
        param = TESTFOLDER + '/input_object.yaml'
        assert cli.createObject(verb_struct,
                                obj_struct,
                                'host',
                                param) == params_object

    @patch('cli.requests.get')  # Mock 'requests' module 'get' method.
    def test_runAPiCall(self, mock_get):
        """Mocking using a decorator"""

        load_dotenv()
        API_HOST = os.getenv("API_HOST")
        API_PORT = os.getenv("API_PORT")
        # TODO: change 201 to only creating new resources
        mock_get.return_value.status_code = 201
        params_object = {'name': 'test1', 'mac_address': 'aa:bb:cc:dd:ee'}

        response = cli.runApiCall(API_HOST, API_PORT, 'get', params_object)

        # Assert that the request-response cycle completed successfully.
        self.assertEqual(response.status_code, 201)
