
from abc import ABC, abstractmethod
from person import Person


class Staff(Person, ABC):
    @abstractmethod
    def fee(self, p_value: int) -> float:
        raise NotImplementedError


class Doctor(Staff):
    def fee(self, p_value: int) -> float:
        return 40 + 5 * (p_value % 5)

    def role(self) -> str:
        return "Doctor"


class Nurse(Staff):
    def fee(self, p_value: int) -> float:
        return 10 + (p_value % 3)

    def role(self) -> str:
        return "Nurse"


class Pharmacist(Staff):
    def fee(self, p_value: int) -> float:
        return 5

    def role(self) -> str:
        return "Pharmacist"


class Lecturer(Person):
    def __init__(self, name: str, person_id: int, module_name: str) -> None:
        if not isinstance(module_name, str) or not module_name.strip():
            raise ValueError("A lecturer must have a module name.")
        self._module_name = module_name.strip()
        super().__init__(name, person_id)

    @property
    def module_name(self) -> str:
        return self._module_name

    def role(self) -> str:
        return "Lecturer"


class MedicalLecturer(Doctor, Lecturer):
    def __init__(self, name: str, person_id: int, module_name: str) -> None:
        super().__init__(name, person_id, module_name)

    def role(self) -> str:
        return "Doctor and Lecturer"
