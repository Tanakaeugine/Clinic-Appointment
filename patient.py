
from abc import abstractmethod
from person import Person


class Patient(Person):
    def payment_factor(self) -> float:
        return 1.0

    def patient_category(self) -> str:
        return "Visitor"

    def role(self) -> str:
        return "Patient"


class StudentPatient(Patient):
    def payment_factor(self) -> float:
        return 0.50

    def patient_category(self) -> str:
        return "Student"


class StaffMemberPatient(Patient):
    def payment_factor(self) -> float:
        return 0.0

    def patient_category(self) -> str:
        return "Staff member"


class VisitorPatient(Patient):
    def payment_factor(self) -> float:
        return 1.0

    def patient_category(self) -> str:
        return "Visitor"
