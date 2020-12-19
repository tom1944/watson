import unittest

from load_session import load_session
from test.fixture.session import ExpectedSession


class TestLoadSession(unittest.TestCase):
    def test_load_session(self):
        session = load_session('test/fixture/session.json')
        expected_session = ExpectedSession.session
        self.assertEqual(session, expected_session)
