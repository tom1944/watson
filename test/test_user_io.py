from unittest import TestCase
from unittest.mock import patch

import user_io
from load_game_config import load_game_config
from test.fixture.context import Cards
from knowledge import Knowledge
from watson import Watson
from user_io import WatsonShell


class TestUserIO(TestCase):
    def test_do_card(self):
        context, session = load_game_config('test/fixture/game_config.json')
        watson = Watson(context, session)
        shell = WatsonShell(watson)
        shell.onecmd("card Tom Roodhart")
        self.assertEqual(watson.knowledge_tables.get(watson.context.players[0], Cards.ROODHART),
                         Knowledge.TRUE)
        for i in range(len(watson.context.players)):
            if i > 0:
                self.assertEqual(
                    watson.knowledge_tables.get(watson.context.players[i], Cards.ROODHART),
                    Knowledge.FALSE)

    reply_string1 = "Tom n"
    reply_string2 = "Michiel y"
    end_string = "done"

    @patch('builtins.input', side_effect=[reply_string1, reply_string2, end_string])
    def test_do_rumour(self, mock_inputs):
        context, session = load_game_config('test/fixture/game_config.json')
        watson = Watson(context, session)
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

