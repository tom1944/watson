from context import Context
from knowledge import Knowledge
from player import Player
from rumour import Rumour
from session import Session
from test.fixture.context import Cards


class ExpectedGameConfig:
    player1 = Player("Tom", "Roodhart", 6)
    player2 = Player("Menno", "Blaauw van Draet", 6)
    player3 = Player("Michiel", "De Wit", 6)

    cards = [Cards.MES, Cards.KANDELAAR, Cards. PISTOOL, Cards.VERGIF, Cards.TOUW,
             Cards.KNUPPEL, Cards.BIJL, Cards.HALTER, Cards.HAL, Cards.EETKAMER,
             Cards.KEUKEN, Cards.WERKKAMER, Cards.THEATER, Cards.ZITKAMER,
             Cards.BUBBELBAD, Cards.GASTENVERBLIJF, Cards.PIMPEL, Cards.GROENEWOUD,
             Cards.BLAAUWVANDRAET, Cards.ROODHART, Cards.DEWIT]

    context = Context([player1, player2, player3], cards)

    cards_seen = {player1: [Cards.ROODHART, Cards.GROENEWOUD, Cards.KEUKEN, Cards.THEATER, Cards.KNUPPEL],
                  player2: [],
                  player3: []}
    rumours = [Rumour(player2, [Cards.MES, Cards.HAL, Cards.PIMPEL], [(player1, Knowledge.TRUE),
                                                                      (player3, Knowledge.FALSE)])]
    session = Session(context, cards_seen, rumours)
