import pytest
import os

import git2image as g2i

def test_checkArgs():
    # TODO: Change this
    docker_test_user = "angelalonso"
    parser = g2i.createParser()
    parsed_test = parser.parse_args(['--directory', 'test', '--dockeruser', docker_test_user])
    assert g2i.checkArgs(parsed_test, parser) == 'test'
    # TODO: test also getting the error for no dockeruser
    parsed_empty = parser.parse_args(['--dockeruser', docker_test_user])
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
    assert g2i.getVersionFromFile("./test/VERSION") != "0.02"
    assert g2i.getVersionFromFile("./test/VERSION") == "0.01"

def test_doVersionsMatch():
    assert g2i.doVersionsMatch("./test/VERSION", "0.01")
    assert not g2i.doVersionsMatch("./test/VERSION", "0.02")

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
