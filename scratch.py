from enum import Enum


characterNames = {
                    'geel': "Van Geelen",
                    'paars': "Pimpel",
                    'groen': "Groenewoud",
                    'blauw': "Blaauw van Draet",
                    'rood': "Roodhart",
                    'wit': "De Wit"
                    }
weaponNames = ['mes', 'kandelaar', 'pistool', 'vergif', 'trofee', 'touw', 'knuppel', 'bijl', 'halter']
roomNames = ['hal', 'eetkamer', 'keuken', 'terras', 'werkkamer', 'theater', 'zitkamer', 'bubbelbad', 'gastenverblijf']
allNames = list(characterNames.keys()) + list(characterNames.values()) + weaponNames + roomNames


class Card:
    def __init__(self, name, category):
        self.name = name
        self.category = category


class Player:
    def __init__(self, name, character, cardAmount):
        self.name = name
        self.character = character
        self.cardAmount = cardAmount


class Knowledge(Enum):
    TRUE = "True"
    FALSE = "False"
    MAYBE = "Maybe"

    @staticmethod
    def fromBool(boolean):
        if boolean:
            return Knowledge.TRUE
        else:
            return Knowledge.FALSE


class Claim:
    def __init__(self, claimer, weapon, room, suspect):
        self.claimer = claimer  # Degene die de claim doet
        self.weapon = weapon
        self.room = room
        self.suspect = suspect
        self.replies = {}  # player -> bool arrray       event.replies[Jan] = False; event.replies[Klaas] = False; event.replies[Mien] = True

    def getCards(self):
        return [self.weapon, self.room, self.suspect]

    # Did player have any of the cards in the claim?
    # Returns Knowledge
    def playerReply(self, player):
        if player in self.replies:
            return Knowledge.fromBool(self.replies[player])
        else:
            return Knowledge.maybe


def getInput(prompt, possibilities):
    userInput = input(prompt)
    """" Suggestie: return een lege array alse de userInput "cancel" is.
         Op die manier kun je een verkeerd getypte outcome cancellen
    """
    if userInput == "cancel":
        return ""

    userInput = userInput.split(", ")
    outcomes = []
    for i in userInput:
        matches = []
        for possibleMatch in possibilities:
            if possibleMatch.lower().startswith(i.lower()):
                matches.append(possibleMatch)
        if len(matches) == 0:
            outcomes.extend(getInput('Could not interpret ' + i + '. Please try again: ', possibilities))
        elif len(matches) == 1:
            outcomes.append(matches[0])
        else:
            found = False
            for possibleMatch in possibilities:
                if possibleMatch.lower() == i.lower():
                    outcomes.append(i)
                    found = True
            if not found:
                outcomes.extend(getInput('Could not interpret ' + i +'. Did you mean: ' + ", ".join(matches) + '? ', possibilities))
    return outcomes

characterCards = [Card(c, "Character") for c in list(characterNames.values())]
weaponCards = [Card(c, "Weapon") for c in weaponNames]
roomCards = [Card(c, "Room") for c in roomNames]
allCards = characterCards + weaponCards + roomCards


def matchCard(cardName):
    for card in allCards:
        if cardName == card.name:
            return card


def startGame():
    playerDecks = {}
    claimHistory = []
    players = []

    playerNames = input('Who are you and who are you playing with? (your name, player 2, player 3, ...)')
    playerNames = playerNames.split(", ")

    for playerName in playerNames:
        character = getInput('Which character is ' + playerName + '?', list(characterNames.keys()) + list(characterNames.values()))[0]
        cardAmount = int(input('How many cards does ' + playerName + ' have?'))
        thePlayer = Player(playerName,character,cardAmount)
        players.append(thePlayer)
        playerDecks[thePlayer] = {}
        for card in allCards:
            playerDecks[thePlayer][card] = 'maybe'

    yourCards = getInput('Which cards do you have? (card 1, card 2, card 3, ...)', allNames)
    yourCards = [matchCard(c) for c in yourCards]
    for card in yourCards:
        playerDecks[players[0]][card]=Knowledge.maybe

    for card in yourCards:
        print(playerDecks[players[0]][card])



if __name__ == "__main__":
    startGame()
