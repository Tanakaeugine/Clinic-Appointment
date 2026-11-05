"""Identity primitives shared by patients and clinic personnel."""
from abc import ABC, abstractmethod


class Person(ABC):
    constructor_calls = 0

    def __init__(self, name: str, person_id: int) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("A person's name cannot be empty.")
        if isinstance(person_id, bool) or not isinstance(person_id, int) or person_id <= 0:
            raise ValueError("A person ID must be a positive integer.")

        Person.constructor_calls += 1
        self._name = name.strip()
        self._person_id = person_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def person_id(self) -> int:
        return self._person_id

    @abstractmethod
    def role(self) -> str:
        """Return the person's clinic-facing role."""
        raise NotImplementedError
