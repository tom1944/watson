import sys

from source.io.watson_shell import WatsonShell
from source.logic.watson import Watson
from source.serialize.load_clues import load_clues


def main():
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
    else:
        filepath = input('Please enter a filepath for loading and saving your session: ')
    clues = None
    while not clues:
        try:
            clues = load_clues(filepath)
        except IOError:
            filepath = input('Cannot seem to open the file, please enter a new filepath: ')

    watson = Watson(clues.context)
    watson.add_info_from_clues(clues)
    shell = WatsonShell(watson, filepath)
    shell.cmdloop()


if __name__ == "__main__":
    main()
