import unittest
from io import StringIO

from source.data.knowledge import Knowledge
from source.data.rumour import Rumour
from source.data.session import Session

from source.serialize.load_session import load_session
from source.serialize.save_session import save_session_to_file_object
from test.fixture.context import context_fixture, Cards, tom, menno, michiel


PATH_OF_SERIALIZED_SESSION = 'test/serialize/session.json'


class TestSerialization(unittest.TestCase):
    def setUp(self):
        self.make_session_fixture()

    def make_session_fixture(self):
        session = Session(context_fixture)
        cards_tom = [Cards.ROODHART, Cards.GROENEWOUD, Cards.KEUKEN, Cards.THEATER, Cards.KNUPPEL]

        for c in cards_tom:
            session.add_card(c, tom)

        session.add_rumour(Rumour(
            claimer=menno,
            rumour_cards=[Cards.MES, Cards.HAL, Cards.PIMPEL],
            replies=[
                (tom, Knowledge.TRUE),
                (michiel, Knowledge.FALSE)
            ]
        ))

        self.session = session

    def test_load_session(self):
        session = load_session(PATH_OF_SERIALIZED_SESSION)
        expected_session = self.session
        self.assertEqual(session, expected_session)

    def test_save_session(self):
        with open(PATH_OF_SERIALIZED_SESSION, 'r') as file:
            reference_serialized_session = file.read()

        with StringIO() as in_memory_stream:

            save_session_to_file_object(
                session=self.session,
                file_object=in_memory_stream
            )
            serialized_session = in_memory_stream.getvalue()

        self.assertEqual(reference_serialized_session, serialized_session)
