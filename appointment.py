
from enum import Enum


class AppointmentStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class Appointment:

    DURATION_HOURS = 1

    def __init__(self, appointment_id: int, patient, staff, start_hour: int) -> None:
        if isinstance(appointment_id, bool) or not isinstance(appointment_id, int) or appointment_id <= 0:
            raise ValueError("Appointment ID must be a positive integer.")
        if isinstance(start_hour, bool) or not isinstance(start_hour, int) or not 0 <= start_hour < 168:
            raise ValueError("Start hour must be an integer from 0 to 167.")
        if patient is None or staff is None:
            raise ValueError("An appointment requires a patient and a staff member.")

        self._appointment_id = appointment_id
        self._patient = patient
        self._staff = staff
        self._start_hour = start_hour
        self._status = AppointmentStatus.PENDING
        self._cancellation_reason = None

    @property
    def appointment_id(self):
        return self._appointment_id

    @property
    def patient(self):
        return self._patient

    @property
    def staff(self):
        return self._staff

    @property
    def start_hour(self):
        return self._start_hour

    @property
    def status(self):
        return self._status

    @property
    def cancellation_reason(self):
        return self._cancellation_reason

    def confirm(self) -> None:
        if self._status is not AppointmentStatus.PENDING:
            raise ValueError("Only a pending appointment can be confirmed.")
        self._status = AppointmentStatus.CONFIRMED

    def cancel(self, current_hour: int, reason: str = "No reason supplied") -> None:
        if self._status is AppointmentStatus.CANCELLED:
            raise ValueError("Appointment is already cancelled.")
        if current_hour >= self._start_hour:
            raise ValueError("Cannot cancel an appointment that has started.")
        if self._status is AppointmentStatus.CONFIRMED and self._start_hour - current_hour < 2:
            raise ValueError("Confirmed appointments require at least 2 hours' notice.")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("A cancellation reason is required.")
        self._status = AppointmentStatus.CANCELLED
        self._cancellation_reason = reason.strip()

    def calculate_fee(self, p_value: int) -> float:
        return self._staff.fee(p_value) * self._patient.payment_factor()
