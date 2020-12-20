from knowledge import Knowledge
from rumour import Rumour
from session import Session
from test.fixture.context import Cards, context, tom, michiel, menno


class ExpectedSession:
    session = Session(
        context=context,
        cards_seen={
            tom: [Cards.ROODHART, Cards.GROENEWOUD, Cards.KEUKEN, Cards.THEATER, Cards.KNUPPEL],
            menno: [],
            michiel: []
        },
        rumours=[Rumour(
            claimer=menno,
            rumour_cards=[Cards.MES, Cards.HAL, Cards.PIMPEL],
            replies=[
                (tom, Knowledge.TRUE),
                (michiel, Knowledge.FALSE)
            ]
        )]
    )
