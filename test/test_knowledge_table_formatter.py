from unittest import TestCase

from card import Cards
from knowledge import Knowledge
from knowledge_table_formatter import KnowledgeTableFormatter
from load_game_state import load_game_state
from watson import Watson


class TestKnowledgeTable(TestCase):
    def test_format_knowledge_table(self):
        watson = Watson(load_game_state('test/game_config.json'))
        watson.knowledge_tables[Cards.EETKAMER.category][watson.game_state.players[0]][Cards.EETKAMER] = Knowledge.FALSE
        watson.knowledge_tables[Cards.ROODHART.category][watson.game_state.players[2]][Cards.ROODHART] = Knowledge.TRUE
        printer = KnowledgeTableFormatter(watson.game_state)
        result = printer.format_knowledge_table(watson.knowledge_tables)

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
