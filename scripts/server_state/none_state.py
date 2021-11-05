import re


class NoneState():
    def __init__(self):
        # Format: `LOGIN <username> <password>`
        # Example: `LOGIN e-gov-vote-kifuwarabe floodgate-300-10F,password`
        self._login_pattern = re.compile(
            r'^LOGIN ([0-9A-Za-z_-]{0,32}) ([0-9A-Za-z_-]{0,32})$')
        self._user_name = ''
        self._password = ''

    @property
    def name(self):
        return "[None]"

    @property
    def user_name(self):
        return self._user_name

    @property
    def password(self):
        return self._password

    def listen_line(self, line):
        matched = self._login_pattern.match(line)
        if matched:
            # ログイン
            self._user_name = matched.group(1)
            self._password = matched.group(2)
            return '<NoneState.Login/>'

        return '<NoneState.Unknown/>'
