import unittest

from source.serialize.load_session import load_session
from test.fixture.session import ExpectedSession, PATH_OF_SERIALIZED_SESSION_FIXTURE


class TestLoadSession(unittest.TestCase):
    def test_load_session(self):
        session = load_session(PATH_OF_SERIALIZED_SESSION_FIXTURE)
        expected_session = ExpectedSession.session
        self.assertEqual(session, expected_session)
