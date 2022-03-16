import unittest
from ds_messenger import DirectMessenger

class DirectMessenger_Test(unittest.TestCase):
    def test_join(self):
        """
        unit test for DirectMessager
        """
        dm=DirectMessenger()
        self.assertIsNotNone(dm.token)
        self.assertTrue(dm.send("msg", "blahblahblah"))
        self.assertEqual(dm.new(), "{\"token\":\""+dm.token+"\", \"directmessage\": \"new\"}")
        self.assertEqual(dm.all(), "{\"token\":\""+dm.token+"\", \"directmessage\": \"all\"}")
        
if __name__ == "__main__":
    unittest.main()
