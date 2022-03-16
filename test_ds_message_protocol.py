import unittest
import ds_message_protocol


class DirectMessageProtocol_Test(unittest.TestCase):
    def test_extract_json(self):
        """
        unit test for DirectMessageProtocol
        """
        string="{\"response\": {\"type\": \"ok\", \"messages\": [{\"message\":\"Hello User 1!\", \"from\":\"markb\", \"timestamp\":\"1603167689.3928561\"},{\"message\":\"Bzzzzz\", \"from\":\"thebeemoviescript\", \"timestamp\":\"1603167689.3928561\"}]}}"
        extracted=ds_message_protocol.extract_json(string)
        self.assertEqual(extracted.type, "ok")
        self.assertEqual(extracted.token, "")
        self.assertEqual(extracted.message[0], ('1603167689.3928561', 'markb', 'Hello User 1!'))
        self.assertEqual(extracted.message[1], ('1603167689.3928561', 'thebeemoviescript', 'Bzzzzz'))

if __name__ == "__main__":
    unittest.main()
