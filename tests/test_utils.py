import unittest


class UtilTest(unittest.TestCase):
    def test_operator_detect(self):
        from pymesomb.utils import detect_operator

        self.assertEqual(detect_operator('677559230'), 'MTN')
        self.assertEqual(detect_operator('237677559230'), 'MTN')
        self.assertEqual(detect_operator('690090980'), 'ORANGE')
        self.assertEqual(detect_operator('237690090980'), 'ORANGE')