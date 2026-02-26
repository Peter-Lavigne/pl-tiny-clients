from pl_mocks_and_fakes import Fake, mock_for

from pl_tiny_clients.current_time import current_time


class TimeFake(Fake):
    def __init__(self) -> None:
        def _current_time_side_effect() -> float:
            result = self.current_time_timestamp
            self.current_time_timestamp += self.tick
            return result

        self.current_time_timestamp: float = 0
        self.tick: float = 0

        mock_for(current_time).side_effect = _current_time_side_effect

    def set_current_time(self, timestamp: float) -> None:
        self.current_time_timestamp = timestamp

    def set_tick(self, tick: float) -> None:
        self.tick = tick
