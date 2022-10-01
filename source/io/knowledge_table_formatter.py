from source.domain.card import Category
from source.domain.knowledge import Knowledge
from source.domain.knowledge_table import KnowledgeTable
from source.io.table_formatter import TableFormatter


def knowledge_to_str(knowledge: Knowledge) -> str:
    return {
        Knowledge.TRUE: 'v',
        Knowledge.FALSE: 'x',
        Knowledge.MAYBE: '.',
    }[knowledge]


class KnowledgeTableFormatter:

    def format_knowledge_table(self, knowledge_table: KnowledgeTable):
        lines = []
        for category in Category:
            lines.append(self.format_category_table(category, knowledge_table))
        return "\n\n".join(lines)

    def format_category_table(self, category: Category, knowledge_table: KnowledgeTable):
        players = knowledge_table.players
        category_cards = [card for card in knowledge_table.cards if card.category == category]
        category_cards.sort(key=lambda card: card.name)

        table = TableFormatter(len(category_cards) + 1, len(players) + 1)
        # Set the player names in the table
        for p in range(len(players)):
            table.set(0, p + 1, players[p].name)
        # Set the card names in the table
        for c in range(len(category_cards)):
            table.set(c + 1, 0, category_cards[c].name)
        # fill the table
        for card_i in range(len(category_cards)):
            for player_i in range(len(players)):
                card = category_cards[card_i]
                player = players[player_i]
                s = knowledge_to_str(knowledge_table.get(player, card))
                table.set(card_i + 1, player_i + 1, s)
        return table.to_string()
