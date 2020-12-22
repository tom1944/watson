from source.data.knowledge import Knowledge
from source.data.rumour import Rumour
from source.data.session import Session
from test.fixture.context import Cards, context_fixture, tom, michiel, menno


def make_session_fixture() -> Session:
    session = Session(context_fixture)
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
