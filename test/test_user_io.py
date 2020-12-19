from unittest import TestCase
from unittest.mock import patch

import user_io
from knowledge import Knowledge
from test.fixture.context import Cards
from test.fixture.session import ExpectedSession
from user_io import WatsonShell
from watson import Watson


class TestUserIO(TestCase):
    def test_do_card(self):
        session = ExpectedSession.session
        watson = Watson(session)
        shell = WatsonShell(watson)
        shell.onecmd("card Tom Roodhart")
        self.assertEqual(watson.get_knowledge_table().get(session.get_context().players[0], Cards.ROODHART),
                         Knowledge.TRUE)
        for i in range(len(watson.context.players)):
            if i > 0:
                self.assertEqual(
                    watson.get_knowledge_table().get(session.get_context().players[i], Cards.ROODHART),
                    Knowledge.FALSE)

    reply_string1 = "Tom n"
    reply_string2 = "Michiel y"
    end_string = "done"

    @patch('builtins.input', side_effect=[reply_string1, reply_string2, end_string])
    def test_do_rumour(self, mock_inputs):
        session = ExpectedSession.session
        watson = Watson(session)
        shell = WatsonShell(watson)
        shell.onecmd("r Menno rood bijl eetkamer")
        rumour = watson.session.rumours[1]
        replies = rumour.replies
        self.assertEqual(set(rumour.rumour_cards), {Cards.ROODHART, Cards.BIJL, Cards.EETKAMER})
        self.assertEqual(rumour.claimer, watson.context.players[1])
        self.assertEqual(replies[0], (watson.context.players[0], Knowledge.FALSE))
        self.assertEqual(replies[1], (watson.context.players[2], Knowledge.TRUE))

    def test_match_input_string_from_set(self):
        result = user_io.match_input_string_from_set("hon", ["bak", "gast", "matig"])
        self.assertEqual(None, result)
        result = user_io.match_input_string_from_set("hon", ["hond", "gast", "matig"])
        self.assertEqual("hond", result)
        result = user_io.match_input_string_from_set("hond", ["hond", "honden", "matig"])
        self.assertEqual("hond", result)
        result = user_io.match_input_string_from_set("hon", ["hond", "honden", "matig"])
        self.assertEqual(None, result)

