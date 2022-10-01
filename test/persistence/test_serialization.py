import unittest
from io import StringIO

from source.domain.knowledge import Knowledge
from source.domain.rumour import Rumour
from source.domain.clues import Clues

from source.persistence.load_clues import load_clues
from source.persistence.save_clues import save_clues_to_file_object
from test.fixture.context import context_fixture, Cards, tom, menno, michiel


PATH_OF_SERIALIZED_CLUES = 'test/persistence/clues.json'


class TestSerialization(unittest.TestCase):
    def setUp(self):
        self.make_clues_fixture()

    def make_clues_fixture(self):
        clues = Clues(context_fixture)
        cards_tom = [Cards.ROODHART, Cards.GROENEWOUD, Cards.KEUKEN, Cards.THEATER, Cards.KNUPPEL]

        for c in cards_tom:
            clues.add_card(c, tom)

        clues.add_rumour(Rumour(
            claimer=menno,
            rumour_cards=[Cards.MES, Cards.HAL, Cards.PIMPEL],
            replies=[
                (tom, Knowledge.TRUE),
                (michiel, Knowledge.FALSE)
            ]
        ))

        self.clues = clues

    def test_load_clues(self):
        clues = load_clues(PATH_OF_SERIALIZED_CLUES)
        expected_clues = self.clues
        self.assertEqual(clues, expected_clues)

    def test_save_clues(self):
        with open(PATH_OF_SERIALIZED_CLUES, 'r') as file:
            reference_serialized_clues = file.read()

        with StringIO() as in_memory_stream:

            save_clues_to_file_object(
                clues=self.clues,
                file_object=in_memory_stream
            )
            serialized_clues = in_memory_stream.getvalue()

        self.assertEqual(reference_serialized_clues, serialized_clues)
