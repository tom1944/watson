from unittest import TestCase
from unittest.mock import patch, create_autospec, Mock

from source.data.knowledge import Knowledge
from source.data.rumour import Rumour
from source.io import watson_shell
from source.io.watson_shell import WatsonShell
from source.logic.watson import Watson
from test.fixture.context import Cards, context_fixture, tom, menno, michiel


class TestWatsonShell(TestCase):
    def setUp(self):
        self.context = context_fixture
        self.watson_mock = create_autospec(
            Watson,
            spec_set=True,
            instance=True,
        )
        self.watson_mock.get_context = Mock(return_value=context_fixture)
        self.shell = WatsonShell(self.watson_mock)

    def test_get_context(self):
        watson = Watson(self.context)
        self.assertEqual(self.context, watson.get_context())

    def test_do_card(self):
        self.shell.onecmd("card Tom Roodhart")
        self.watson_mock.add_knowledge.assert_called_with(tom, Cards.ROODHART, Knowledge.TRUE)

    @patch('builtins.input', side_effect=["Tom n", "Michiel y", "done"])
    def test_do_rumour(self, mock_inputs):
        self.shell.onecmd("r Menno rood bijl eetkamer")

        reference_rumour = Rumour(
            menno,
            [Cards.ROODHART, Cards.BIJL, Cards.EETKAMER],
            replies=[
                (tom, Knowledge.FALSE),
                (michiel, Knowledge.TRUE),
            ]
        )

        self.watson_mock.add_rumour.assert_called_with(reference_rumour)

    @patch('builtins.input', side_effect=["wrong n", "Tom n", "Michiel y", "done"])
    def test_do_rumour_faulty_input(self, mock_inputs):
        self.shell.onecmd("r Menno rood bijl eetkamer")

        reference_rumour = Rumour(
            menno,
            [Cards.ROODHART, Cards.BIJL, Cards.EETKAMER],
            replies=[
                (tom, Knowledge.FALSE),
                (michiel, Knowledge.TRUE),
            ]
        )

        self.watson_mock.add_rumour.assert_called_with(reference_rumour)

    def test_match_input_string_from_set(self):
        result = watson_shell.match_input_string_from_set("hon", ["bak", "gast", "matig"])
        self.assertEqual(None, result)

        result = watson_shell.match_input_string_from_set("hon", ["hond", "gast", "matig"])
        self.assertEqual("hond", result)

        result = watson_shell.match_input_string_from_set("hond", ["hond", "honden", "matig"])
        self.assertEqual("hond", result)

        result = watson_shell.match_input_string_from_set("hon", ["hond", "honden", "matig"])
        self.assertEqual(None, result)

        result = watson_shell.match_input_string_from_set("hal", ["Halter", "Hal"])
        self.assertEqual(None, result)

