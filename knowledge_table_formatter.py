import watson
from card import Category
from gamestate import GameState
from knowledge import Knowledge
from knowledge_table import KnowledgeTable
from table_formatter import TableFormatter


class KnowledgeTableFormatter:
    game_state: GameState

    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def format_knowledge_table(self, knowledge_table: KnowledgeTable):
        lines = []
        for category in Category:
            lines.append(self.format_category_table(category, knowledge_table))
        return "\n".join(lines)

    def format_category_table(self, category: Category, knowledge_table: KnowledgeTable):
        players = self.game_state.players
        category_cards = [card for card in self.game_state.used_cards if card.category == category]
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
                s = self.knowledge_to_str(knowledge_table[card.category][player][card])
                table.set(card_i + 1, player_i + 1, s)
        return table.to_string()

    def knowledge_to_str(self, knowledge: Knowledge) -> str:
        return {
            Knowledge.TRUE: 'v',
            Knowledge.FALSE: 'x',
            Knowledge.MAYBE: '.',
        }[knowledge]

