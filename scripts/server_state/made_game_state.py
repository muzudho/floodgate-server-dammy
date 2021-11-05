import re


class MadeGameState():
    """対局が付いた"""

    def __init__(self):
        pass

    @property
    def name(self):
        return "<MadeGameState/>"

    def parse_line(self, line):
        return '<MadeGameState.Unknown/>'
