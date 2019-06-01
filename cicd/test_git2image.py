import pytest

import git2image as g2i

def test_getConfig():
    filename = 'apps.json'
    data = {}  
    data['frontend'] = {  
        'dir': 'applications/frontend',
        'version': '0.1'
    }
    data['backend'] = {  
        'dir': 'applications/backend',
        'version': '0.1'
    }
    json = g2i.getConfig(filename)
    assert data == json

def test_getMasterChanges():
    pass

def test_checkVersion():
    pass

def test_runTest():
    pass

def test_buildImage():
    pass

def test_pushImage():
    pass
