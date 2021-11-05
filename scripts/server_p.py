from scripts.server_state.none_state import NoneState
from scripts.server_state.made_game import MadeGame
from scripts.log_output import log_output


class ServerP():
    """サーバーパーサー"""

    def __init__(self):
        self._state = NoneState()

    def listen_line(self, line):
        result = self._state.listen_line(line)

        if self._state == '[None]':
            if result == '<NoneState.Login/>':
                log_output.display_and_log_internal(
                    f'Login user_name=[{self._state.user_name}] password=[{self._state.password}]')

                # TODO ２人以上のユーザーがログインしていて、マッチングに成功したとします

                self._state = MadeGame()

        elif self._state == '[MadeGame]':
            pass
        else:
            pass

        log_output.display_and_log_internal(result)


if __name__ == "__main__":
    """テストします"""
    line = 'LOGIN:egov-kifuwarabe OK'

    server_p = ServerP()
    result = server_p.listen_line(line)
    if result == '<NoneState.Login/>':
        print('.', end='')
    else:
        print('f', end='')
