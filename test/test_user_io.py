from unittest import TestCase
from unittest.mock import patch

from source.data.session import Session
from source.io import user_io
from source.data.knowledge import Knowledge
from test.fixture.context import Cards, context_fixture
from source.io.user_io import WatsonShell
from source.logic.watson import Watson


class TestUserIO(TestCase):
    def setUp(self):
        self.session = Session(context_fixture)
        self.watson = Watson(self.session)
        self.shell = WatsonShell(self.watson)

    def test_do_card(self):
        self.shell.onecmd("card Tom Roodhart")
        knowledge_table = self.watson.get_knowledge_table()
        self.assertEqual(knowledge_table.get(self.session.get_context().players[0], Cards.ROODHART),
                         Knowledge.TRUE)
        for i in range(len(self.session.get_context().players)):
            if i > 0:
                self.assertEqual(
                    knowledge_table.get(self.session.get_context().players[i], Cards.ROODHART),
                    Knowledge.FALSE)

    @patch('builtins.input', side_effect=["Tom n", "Michiel y", "done"])
    def test_do_rumour(self, mock_inputs):
        self.shell.onecmd("r Menno rood bijl eetkamer")
        rumour = self.session.get_rumours()[0]
        replies = rumour.replies
        self.assertEqual(set(rumour.rumour_cards), {Cards.ROODHART, Cards.BIJL, Cards.EETKAMER})
        self.assertEqual(rumour.claimer, self.watson.context.players[1])
        self.assertEqual(replies[0], (self.watson.context.players[0], Knowledge.FALSE))
        self.assertEqual(replies[1], (self.watson.context.players[2], Knowledge.TRUE))

    def test_match_input_string_from_set(self):
        result = user_io.match_input_string_from_set("hon", ["bak", "gast", "matig"])
        self.assertEqual(None, result)
        result = user_io.match_input_string_from_set("hon", ["hond", "gast", "matig"])
        self.assertEqual("hond", result)
        result = user_io.match_input_string_from_set("hond", ["hond", "honden", "matig"])
        self.assertEqual("hond", result)
        result = user_io.match_input_string_from_set("hon", ["hond", "honden", "matig"])
        self.assertEqual(None, result)
