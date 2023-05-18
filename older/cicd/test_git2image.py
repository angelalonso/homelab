import pytest
import os

import git2image as g2i

def test_checkArgs():
    # TODO: Change this
    parser = g2i.createParser()
    parsed_test = parser.parse_args(['--directory', 'test'])
    assert g2i.checkArgs(parsed_test, parser) == 'test'
    # TODO: test also getting the error for no dockeruser
    parsed_empty = parser.parse_args()
    assert g2i.checkArgs(parsed_empty, parser) == os.getcwd() + "/.."

def test_getConfig():
    filename = './test/apps.json'
    data = {}  
    data['frontend'] = {  
        'dir': 'application/frontend',
        'version': '0.1'
    }
    data['backend'] = {  
        'dir': 'application/backend',
        'version': '0.1'
    }
    json = g2i.getConfig(filename)
    assert json == data

def test_getMasterChanges():
    #NOTE: change this depending on the master path
    test_git_dir = '../'
    gitPullErr = g2i.getMasterChanges(test_git_dir)
    assert gitPullErr == None

def test_getVersionFromFile():
    assert g2i.getVersionFromFile("./test/VERSION") != ""
    assert g2i.getVersionFromFile("./test/VERSION") != "blah"
    assert g2i.getVersionFromFile("./test/VERSION") == "0.00"

def test_getVersionsFromHub():
    test_result = ['0.00']
    assert g2i.getVersionsFromHub('angelalonso/test') == test_result

def test_doVersionsMatch():
    assert g2i.isVersionOnHub("./test", "angelalonso/test")

def test_runTest():
    assert not g2i.runTest("./test")

def test_buildImage():
    assert not g2i.buildImage('test', '0.00', 'test/.')
    assert g2i.buildImage('test', '0.00', 'test/docker/.')

def test_pushImage():
    # TODO: Change this
    docker_test_user = "angelalonso"
    #assert not g2i.pushImage(docker_test_user, 'test', '0.00', 'test/.')
    assert g2i.pushImage(docker_test_user, 'test', '0.00', 'test/docker/.')
