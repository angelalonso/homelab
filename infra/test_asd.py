import pytest

import asd
TESTFOLDER = './testfiles'

class TestAll:
    @classmethod
    def setup_class(cls):
        pass

    def test_getSecrets(self):
        """Must return decoded YAML response."""
        secretsfile = TESTFOLDER + '/secrets_simple.yaml'
        secrets = asd.getSecrets(secretsfile)
        assert secrets == {'groups': {'phase1': {'hosts': ['test01']}, 'raspbian': {'hosts': ['test01']}}, 'hosts': {'test01': {'ansible_ssh_port': 22, 'ansible_user': {'name': 'pi', 'password': 'raspberry'}, 'ip': '192.168.0.1'}}}

    def test_willWeRunPhase1(self):
        # Find out secrets with one phase1-related host
        secretsfile = TESTFOLDER + '/secrets_onehostphase1.yaml'
        secrets = asd.getSecrets(secretsfile)
        assert asd.isPhase1Needed(secrets)[0] == True
        # Find out secrets with more than one phase1-related hosts
        secretsfile = TESTFOLDER + '/secrets_severalhostsphase1.yaml'
        secrets = asd.getSecrets(secretsfile)
        assert asd.isPhase1Needed(secrets)[0] == True
        # Find out secrets without any phase1-related hosts
        secretsfile = TESTFOLDER + '/secrets_nohostsphase1.yaml'
        secrets = asd.getSecrets(secretsfile)
        assert asd.isPhase1Needed(secrets)[0] == False

    def test_generateSeparatedSecrets(self):
        secretsfile = TESTFOLDER + '/secrets_onehostphase1.yaml'
        secrets = asd.getSecrets(secretsfile)
        secrets_phase1 = asd.getPhaseSplittedSecrets(secrets, asd.isPhase1Needed(secrets)[1])
        assert secrets_phase1[0] == {
                'hosts': 
                    {'test01': {'ansible_ssh_port': 22, 'ansible_user': {'name': 'pi', 'password': 'raspberry'}, 'ip': '192.168.0.1'}}, 
                'groups': 
                    {'phase1': {'hosts': ['test01'], 'packages': ['python-apt', 'git', 'vim'], 'phase2_ansible_user': {'name': 'admin', 'password': 'test', 'ssh_key': '/home/admin/.ssh/admin.pub', 'ssh_path': '/home/admin/.ssh', 'ssh_port': 2222}}}}
        assert secrets_phase1[1] == {
                'hosts': 
                    {'test01': {'ansible_ssh_port': 2222, 'ansible_user': {'name': 'admin', 'password': 'test', 'ssh_key': '/home/admin/.ssh/admin.pub', 'ssh_path': '/home/admin/.ssh'}}, 
                    'test02': {'ansible_ssh_port': 2222, 'ansible_user': {'name': 'admin', 'password': 'test'}, 'ip': '192.168.0.2'}}, 
                'groups': 
                    {'raspbian': {'hosts': ['test01', 'test02'], 'packages': ['python-apt', 'git', 'vim']}, 
                    'dockernode': {'hosts': ['test01'], 'docker_users': ['admin']}}}

    def test_generatePhase1Hosts(self):
        pass

    def test_generateOtherHosts(self):
        pass

    def test_generatePhase1Manifests(self):
        pass

    def test_generateOtherManifests(self):
        pass

