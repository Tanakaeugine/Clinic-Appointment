
class ClinicClock:
    def __init__(self, current_hour: int = 0) -> None:
        self.set_hour(current_hour)

    @staticmethod
    def _validate(hour: int) -> None:
        if isinstance(hour, bool) or not isinstance(hour, int) or not 0 <= hour <= 168:
            raise ValueError("Clinic time must be an integer hour from 0 to 168.")

    def now(self) -> int:
        return self._hour

    def set_hour(self, hour: int) -> None:
        self._validate(hour)
        self._hour = hour
