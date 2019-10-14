import unittest
import d8s_controller as d8sc

class HelloworldTests(unittest.TestCase):
    
    def test_get_helloworld(self):
        self.assertEqual(d8sc.get_greetings(), 'Hello World!')

    def test_get_docker_swarm_status(self):
        self.assertEqual(d8sc.get_docker_swarm_status(), [])

if __name__ == '__main__':
    unittest.main()
