from unittest import TestCase

from card import Cards
from knowledge import Knowledge
from knowledge_table import KnowledgeTable
from knowledge_table_formatter import KnowledgeTableFormatter
from load_game_state import load_game_state
from watson import Watson


class TestKnowledgeTable(TestCase):
    def test_format_knowledge_table(self):
        watson = Watson(load_game_state('test/game_config.json'))
        knowledge_table = KnowledgeTable(watson.game_state.players, watson.game_state.used_cards)
        knowledge_table.set_item(Cards.EETKAMER, knowledge_table.players[0], Knowledge.FALSE)
        knowledge_table.set_item(Cards.ROODHART, knowledge_table.players[2], Knowledge.TRUE)
        printer = KnowledgeTableFormatter()
        result = printer.format_knowledge_table(knowledge_table)

        expected = '\n'.join([
            "                   Tom    Menno  Michiel ",
            "Blaauw van Draet    .       .       .    ",
            "          De Wit    .       .       .    ",
            "      Groenewoud    .       .       .    ",
            "          Pimpel    .       .       .    ",
            "        Roodhart    .       .       v    ",
            "",
            "            Tom    Menno  Michiel ",
            "     Bijl    .       .       .    ",
            "   Halter    .       .       .    ",
            "Kandelaar    .       .       .    ",
            "  Knuppel    .       .       .    ",
            "      Mes    .       .       .    ",
            "  Pistool    .       .       .    ",
            "     Touw    .       .       .    ",
            "   Vergif    .       .       .    ",
            "",
            "                 Tom    Menno  Michiel ",
            "     Bubbelbad    .       .       .    ",
            "      Eetkamer    x       .       .    ",
            "Gastenverblijf    .       .       .    ",
            "           Hal    .       .       .    ",
            "        Keuken    .       .       .    ",
            "       Theater    .       .       .    ",
            "     Werkkamer    .       .       .    ",
            "      Zitkamer    .       .       .    ",
            "",
        ])
        self.assertEqual(result, expected)