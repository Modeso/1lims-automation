from unittest import TestCase
from unittest import skip

class test(TestCase):
    @skip('http://github.com/0xislamtaha')
    def test001(self):
        """
            DOCSTRING
        """
        self.assertTrue(True)
