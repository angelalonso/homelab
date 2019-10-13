import unittest
import d8s-controller as d8sc

class HelloworldTests(unittest.TestCase):
    
    def test_get_helloworld(self):
        self.assertEqual(d8sc.get_greetings(), 'Hello World!')

if __name__ == '__main__':
    unittest.main()
