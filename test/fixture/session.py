from knowledge import Knowledge
from rumour import Rumour
from session import Session
from test.fixture.context import Cards, context, tom, michiel, menno


def make_session_fixture() -> Session:
    session = Session(context)
    cards_tom = [Cards.ROODHART, Cards.GROENEWOUD, Cards.KEUKEN, Cards.THEATER, Cards.KNUPPEL]

    for c in cards_tom:
        session.add_card(c, tom)

    session.add_rumour(Rumour(
        claimer=menno,
        rumour_cards=[Cards.MES, Cards.HAL, Cards.PIMPEL],
        replies=[
            (tom, Knowledge.TRUE),
            (michiel, Knowledge.FALSE)
        ]
    ))

    return session


class ExpectedSession:
    session = make_session_fixture()
