import unittest
from io import StringIO

from source.serialize.save_session import save_session_to_file_object
from test.fixture.session import ExpectedSession, PATH_OF_SERIALIZED_SESSION_FIXTURE


class TestSaveSession(unittest.TestCase):
    def test_save_session(self):
        with open(PATH_OF_SERIALIZED_SESSION_FIXTURE, 'r') as file:
            reference_serialized_session = file.read()

        with StringIO() as in_memory_stream:

            save_session_to_file_object(
                session=ExpectedSession.session,
                file_object=in_memory_stream
            )
            serialized_session = in_memory_stream.getvalue()

        self.assertEqual(reference_serialized_session, serialized_session)
