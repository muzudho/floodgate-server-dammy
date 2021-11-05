from scripts.server_state.none_state import NoneState
from scripts.server_state.made_game_state import MadeGameState
from scripts.log_output import log_output


class ServerP():
    """サーバーパーサー"""

    def __init__(self):
        self._state = NoneState()

    def parse_line(self, line):
        print(f"parse_line: line=[{line}]")

        result = self._state.parse_line(line)

        log_output.display_and_log_internal(
            f"Before: self._state.name=[{self._state.name}] result=[{result}]")

        if self._state.name == '<None/>':
            if result == '<NoneState.Login/>':
                log_output.display_and_log_internal(
                    f'Login user_name=[{self._state.user_name}] password=[{self._state.password}]')

                # TODO ２人以上のユーザーがログインしていて、マッチングに成功したとします

                self._state = MadeGameState()

        elif self._state.name == '<MadeGameState/>':
            pass
        else:
            pass

        log_output.display_and_log_internal(
            f"After: self._state.name=[{self._state.name}]")


if __name__ == "__main__":
    """テストします"""
    line = 'LOGIN:egov-kifuwarabe OK'

    server_p = ServerP()
    result = server_p.parse_line(line)
    if result == '<NoneState.Login/>':
        print('.', end='')
    else:
        print('f', end='')
