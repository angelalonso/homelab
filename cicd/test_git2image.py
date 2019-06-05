import pytest
import os

import git2image as g2i

def test_checkArgs():
    parsed_test = g2i.createParser().parse_args(['--directory', 'test'])
    assert g2i.checkArgs(parsed_test) == 'test'
    parsed_empty = g2i.createParser().parse_args([])
    assert g2i.checkArgs(parsed_empty) == os.getcwd() + "/.."

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

def test_checkVersionsMatch():
    assert g2i.checkVersionsMatch("./test/VERSION", "0.01")
    assert not g2i.checkVersionsMatch("./test/VERSION", "0.02")

def test_runTest():
    assert not g2i.runTest("./test")

def test_buildImage():
    pass

def test_pushImage():
    pass
