from cmd import Cmd
from typing import List, Optional, Tuple

from source.data.card import Card, Category
from source.data.knowledge import Knowledge
from source.data.player import Player
from source.data.rumour import Rumour
from source.logic.watson import Watson
from source.serialize.save_clues import save_clues_to_file


class WatsonShell(Cmd):
    def __init__(self, watson: Watson, filepath: str = 'clue_log.json', auto_save: bool = False, **kwargs):
        Cmd.__init__(self, **kwargs)
        self.watson = watson
        self.context = watson.get_context()
        self.filepath = filepath
        self.auto_save = auto_save
        self.intro = "Welcome to Watson, the Cluedo assistant. Type help or ? to list commands.\n"
        self.prompt = ">>> "

    def preloop(self) -> None:
        print(self.watson.display_state())

    def do_card(self, arg):
        """"card <owner> <card> """
        args = arg.split(maxsplit=1)

        if len(args) != 2:
            print('Usage: ' + str(self.do_card.__doc__))
            return False

        owner_name, card_name = args

        card = match_card(card_name, self.context.cards)
        owner = match_player(owner_name, self.context.players)

        if not card or not owner:
            return False

        self.watson.add_knowledge(owner, card, Knowledge.TRUE)
        print(self.watson.display_state())
        if self.auto_save:
            self.do_save()

    def do_c(self, arg):
        """"Alias for card"""
        self.do_card(arg)

    def do_rumour(self, arg):
        """"rumour <claimer> <card1> <card2> <card3>"""
        args = arg.split()

        if len(args) != 4:
            print('Usage: ' + str(self.do_rumour.__doc__))
            return False

        claimer_name = args[0]
        card_names = args[1:]
        rumour_cards = [match_card(card_name, self.context.cards) for card_name in card_names]
        claimer = match_player(claimer_name, self.context.players)

        if not all(rumour_cards) or not claimer:
            return False

        if not {card.category for card in rumour_cards} == {Category.CHARACTER, Category.ROOM, Category.WEAPON}:
            print("A rumour should contain all categories")
            return False

        replies = self.ask_replies()
        if not replies:
            return False
        rumour = Rumour(claimer, rumour_cards, replies)
        self.watson.add_rumour(rumour)
        print(self.watson.display_state())
        if self.auto_save:
            self.do_save()

    def do_r(self, arg):
        """Alias for rumour"""
        self.do_rumour(arg)

    def do_save(self, arg=''):
        """save [filename]"""
        args = arg.split()

        if len(args) == 0:
            pass
        elif len(args) == 1:
            self.filepath = args[0] + '.json'
        else:
            print('Usage: ' + str(self.do_rumour.__doc__))
            return False

        save_clues_to_file(self.watson.get_clues(), self.filepath)
        print(f'Session saved to {self.filepath}')

    def do_s(self, arg):
        """Alias for save"""
        self.do_save(arg)

    def do_autosave(self, arg):
        """"autosave <on/off>"""
        if arg == 'on':
            self.auto_save = True
        elif arg == 'off':
            self.auto_save = False
        else:
            print('Usage: ' + str(self.do_autosave.__doc__))

    def do_exit(self, arg):
        """Exit the program"""
        if arg != '':
            print('Usage: ' + str(self.do_autosave.__doc__))
            return False
        return True

    def ask_replies(self) -> Optional[List[Tuple[Player, Knowledge]]]:
        replies = []
        while True:
            response = input("     ")
            if response.lower() == "abort":
                return None
            if response.lower() == "done" and replies:
                return replies
            response = response.split()
            if len(response) != 2:
                print("Usage: <Player> <y|n>")
                continue
            player = match_player(response[0], self.context.players)
            if response[1] == "y":
                knowledge = Knowledge.TRUE
            elif response[1] == "n":
                knowledge = Knowledge.FALSE
            else:
                print("Reply should be y or n")
                continue
            replies.append((player, knowledge))


def match_player(start_of_player_name: str, players: List[Player]) -> Optional[Player]:
    player_name = match_input_string_from_set(start_of_player_name, [p.name for p in players])
    if not player_name:
        return None
    return [p for p in players if p.name == player_name][0]


def match_card(start_of_card_name: str, cards: List[Card]) -> Optional[Card]:
    card_name = match_input_string_from_set(start_of_card_name, [c.name for c in cards])
    if not card_name:
        return None
    return [c for c in cards if c.name == card_name][0]


def match_input_string_from_set(start: str, input_set: List[str]) -> Optional[str]:
    matches = [i for i in input_set if i.lower().startswith(start.lower())]
    if len(matches) == 0:
        print(f'Input "{start}" invalid. Choose one of: {", ".join(input_set)}.')
        return None
    elif len(matches) == 1:
        return matches[0]
    elif start in matches:
        return start
    else:
        print(f'Input "{start}" ambiguous. Did you mean one of: {", ".join(matches)}?')
        return None
