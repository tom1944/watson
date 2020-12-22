from unittest import TestCase

from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.io.knowledge_table_formatter import KnowledgeTableFormatter
from test.fixture.context import Cards, context_fixture


class TestKnowledgeTable(TestCase):
    def test_format_knowledge_table(self):
        context = context_fixture
        knowledge_table = KnowledgeTable(context.players, context.cards)
        knowledge_table.set(knowledge_table.players[0], Cards.EETKAMER, Knowledge.FALSE)
        knowledge_table.set(knowledge_table.players[2], Cards.ROODHART, Knowledge.TRUE)

        printer = KnowledgeTableFormatter()
        result = printer.format_knowledge_table(knowledge_table)

        expected = '\n'.join([
            "                   Tom    Menno  Michiel",
            "Blaauw van Draet    .       .       .   ",
            "          De Wit    .       .       .   ",
            "      Groenewoud    .       .       .   ",
            "          Pimpel    .       .       .   ",
            "        Roodhart    .       .       v   ",
            "",
            "            Tom    Menno  Michiel",
            "     Bijl    .       .       .   ",
            "   Halter    .       .       .   ",
            "Kandelaar    .       .       .   ",
            "  Knuppel    .       .       .   ",
            "      Mes    .       .       .   ",
            "  Pistool    .       .       .   ",
            "     Touw    .       .       .   ",
            "   Vergif    .       .       .   ",
            "",
            "                 Tom    Menno  Michiel",
            "     Bubbelbad    .       .       .   ",
            "      Eetkamer    x       .       .   ",
            "Gastenverblijf    .       .       .   ",
            "           Hal    .       .       .   ",
            "        Keuken    .       .       .   ",
            "       Theater    .       .       .   ",
            "     Werkkamer    .       .       .   ",
            "      Zitkamer    .       .       .   ",
        ])
        self.assertEqual(result, expected)
