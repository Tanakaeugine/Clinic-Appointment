
from appointment import Appointment, AppointmentStatus


class Clinic:

    def __init__(self, clock, logger, p_value: int) -> None:
        if isinstance(p_value, bool) or not isinstance(p_value, int) or p_value < 0:
            raise ValueError("P must be a non-negative integer.")
        self._clock = clock
        self._logger = logger
        self._p_value = p_value
        self._patients = {}
        self._staff = {}
        self._appointments = {}
        self._used_ids = set()

    @property
    def patients(self):
        return tuple(self._patients.values())

    @property
    def staff_members(self):
        return tuple(self._staff.values())

    @property
    def appointments(self):
        return tuple(self._appointments.values())

    def _record_failure(self, action: str, error: Exception) -> None:
        try:
            self._logger.write(f"FAILED {action}: {error}")
        except Exception as log_error:
            # A broken journal must not replace the original business error.
            print(f"[log] unable to record failure: {log_error}")

    def _register(self, person, registry, label: str) -> None:
        try:
            if person.person_id in self._used_ids:
                raise ValueError("Duplicate ID.")
            registry[person.person_id] = person
            self._used_ids.add(person.person_id)
            self._logger.write(f"REGISTER {label} #{person.person_id}")
        except Exception as error:
            self._record_failure(f"register {label}", error)
            raise

    def register_patient(self, patient) -> None:
        self._register(patient, self._patients, "patient")

    def register_staff(self, staff) -> None:
        self._register(staff, self._staff, staff.role())

    def book(self, appointment_id: int, patient, staff, start_hour: int) -> Appointment:
        try:
            if patient.person_id not in self._patients or self._patients[patient.person_id] is not patient:
                raise ValueError("Patient is not registered with this clinic.")
            if staff.person_id not in self._staff or self._staff[staff.person_id] is not staff:
                raise ValueError("Staff member is not registered with this clinic.")
            if appointment_id in self._used_ids:
                raise ValueError("Duplicate ID.")
            if start_hour < self._clock.now():
                raise ValueError("Cannot book an appointment in the past.")

            appointment = Appointment(appointment_id, patient, staff, start_hour)
            for existing in self._appointments.values():
                if (existing.status is not AppointmentStatus.CANCELLED
                        and existing.start_hour == start_hour):
                    if existing.patient is patient:
                        raise ValueError("Patient already has an appointment at this hour.")
                    if existing.staff is staff:
                        raise ValueError("Staff member is already booked at this hour.")

            self._appointments[appointment_id] = appointment
            self._used_ids.add(appointment_id)
            self._logger.write(f"BOOK appointment #{appointment_id}")
            return appointment
        except Exception as error:
            self._record_failure(f"book #{appointment_id}", error)
            raise

    def confirm(self, appointment_id: int) -> None:
        appointment = self._get_appointment(appointment_id, "confirm")
        try:
            appointment.confirm()
            self._logger.write(f"CONFIRM appointment #{appointment_id}")
        except Exception as error:
            self._record_failure(f"confirm #{appointment_id}", error)
            raise

    def cancel(self, appointment_id: int, reason: str) -> None:
        appointment = self._get_appointment(appointment_id, "cancel")
        try:
            appointment.cancel(self._clock.now(), reason)
            self._logger.write(f"CANCEL appointment #{appointment_id}: {reason}")
        except Exception as error:
            self._record_failure(f"cancel #{appointment_id}", error)
            raise

    def _get_appointment(self, appointment_id: int, action: str) -> Appointment:
        try:
            return self._appointments[appointment_id]
        except KeyError:
            error = ValueError(f"Appointment #{appointment_id} does not exist.")
            self._record_failure(f"{action} #{appointment_id}", error)
            raise error

    def fee_for(self, appointment_id: int) -> float:
        appointment = self._get_appointment(appointment_id, "calculate fee")
        amount = appointment.calculate_fee(self._p_value)
        self._logger.write(f"CALCULATE fee for appointment #{appointment_id}: {amount:g}")
        return amount
