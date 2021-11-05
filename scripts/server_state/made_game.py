import re


class MadeGame():
    """対局が付いた"""

    def __init__(self):
        pass

    @property
    def name(self):
        return "[MadeGame]"

    def listen_line(self, line):
        return '<MadeGame.Unknown/>'
