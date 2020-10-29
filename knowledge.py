from enum import Enum


class Knowledge(Enum):
    TRUE = "True"
    FALSE = "False"
    MAYBE = "Maybe"

    @staticmethod
    def from_bool(boolean):
        if boolean:
            return Knowledge.TRUE
        else:
            return Knowledge.FALSE
