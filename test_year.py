import unittest
from app import app
from params import Params
from werkzeug.exceptions import NotFound, UnprocessableEntity, BadRequest


class TestYear(unittest.TestCase):

    def setUp(self):
        self.params = Params()
        return super().setUp()

    def tearDown(self):
        self.params = None
        return super().tearDown()

    def test_correct_year(self):
        """
        Test that params accepts correct year and returns nothing
        """
        self.assertIsNone(self.params.year_validate(2013))

    def test_incorrect_year(self):
        """
        Tests that params aborts (422 status) on year  < 2012
        """
        with self.assertRaises(UnprocessableEntity):
            self.params.year_validate(2011)

    def test_non_ints_are_rejected(self):
        """
        Test strings ('abc' as oppsed to '2012), objects, etc should be aborted by params
        """
        params = Params()
        # test string input
        with self.assertRaises(BadRequest):
            params.year_validate('abc')
        #test object input
        with self.assertRaises(BadRequest):
            params.year_validate(params)
        #test bool input
        with self.assertRaises(BadRequest):
            params.year_validate(True)


if __name__ == '__main__':
    unittest.main()