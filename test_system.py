
import tempfile
import unittest
from pathlib import Path

from appointment import AppointmentStatus
from clinic import Clinic
from clock import ClinicClock
from logger import AppointmentLogger
from patient import StudentPatient, StaffMemberPatient, VisitorPatient
from person import Person
from staff import Doctor, Nurse, Pharmacist, MedicalLecturer


class ClinicSystemTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.logger = AppointmentLogger(str(Path(self.temp_dir.name) / "test.log"))
        self.logger.__enter__()
        self.addCleanup(self.logger.__exit__, None, None, None)
        self.clock = ClinicClock(8)
        self.clinic = Clinic(self.clock, self.logger, 7)
        self.student = StudentPatient("Student", 1)
        self.employee = StaffMemberPatient("Employee", 2)
        self.visitor = VisitorPatient("Visitor", 3)
        self.doctor = Doctor("Doctor", 4)
        self.nurse = Nurse("Nurse", 5)
        self.pharmacist = Pharmacist("Pharmacist", 6)
        for patient in (self.student, self.employee, self.visitor):
            self.clinic.register_patient(patient)
        for member in (self.doctor, self.nurse, self.pharmacist):
            self.clinic.register_staff(member)

    def test_fee_formulas_and_discount_policy(self):
        self.assertEqual(self.doctor.fee(7), 50)
        self.assertEqual(self.nurse.fee(7), 11)
        self.assertEqual(self.pharmacist.fee(7), 5)
        self.assertEqual(self.student.payment_factor(), .5)
        self.assertEqual(self.employee.payment_factor(), 0)
        self.assertEqual(self.visitor.payment_factor(), 1)

    def test_discounted_appointment_amounts(self):
        self.clinic.book(20, self.student, self.doctor, 15)
        self.clinic.book(21, self.employee, self.nurse, 16)
        self.clinic.book(22, self.visitor, self.pharmacist, 17)
        self.assertEqual(self.clinic.fee_for(20), 25)
        self.assertEqual(self.clinic.fee_for(21), 0)
        self.assertEqual(self.clinic.fee_for(22), 5)

    def test_patient_and_staff_cannot_be_double_booked(self):
        self.clinic.book(20, self.student, self.doctor, 15)
        with self.assertRaises(ValueError):
            self.clinic.book(21, self.student, self.nurse, 15)
        with self.assertRaises(ValueError):
            self.clinic.book(22, self.visitor, self.doctor, 15)

    def test_cancelled_slot_is_reusable(self):
        self.clinic.book(20, self.student, self.doctor, 15)
        self.clinic.cancel(20, "Change of plans")
        self.clinic.book(21, self.student, self.nurse, 15)

    def test_confirmed_appointment_requires_two_hours_notice(self):
        self.clinic.book(20, self.student, self.doctor, 10)
        self.clinic.confirm(20)
        self.clock.set_hour(9)
        with self.assertRaises(ValueError):
            self.clinic.cancel(20, "Too late")
        self.clock.set_hour(8)
        self.clinic.cancel(20, "Two hours notice")

    def test_cannot_cancel_after_start(self):
        self.clinic.book(20, self.student, self.doctor, 10)
        self.clock.set_hour(10)
        with self.assertRaises(ValueError):
            self.clinic.cancel(20, "Already started")

    def test_cancelled_appointment_is_terminal(self):
        self.clinic.book(20, self.student, self.doctor, 15)
        self.clinic.cancel(20, "Cancelled")
        with self.assertRaises(ValueError):
            self.clinic.confirm(20)
        self.assertEqual(self.clinic.appointments[0].status, AppointmentStatus.CANCELLED)

    def test_unique_ids_across_people_and_appointments(self):
        with self.assertRaises(ValueError):
            self.clinic.register_staff(Doctor("Duplicate", 1))
        self.clinic.book(20, self.student, self.doctor, 15)
        with self.assertRaises(ValueError):
            self.clinic.book(1, self.visitor, self.nurse, 16)

    def test_public_collections_are_snapshots(self):
        self.clinic.book(20, self.student, self.doctor, 15)
        snapshot = self.clinic.appointments
        snapshot = ()
        self.assertEqual(len(self.clinic.appointments), 1)

    def test_medical_lecturer_uses_one_person_constructor(self):
        before = Person.constructor_calls
        lecturer = MedicalLecturer("Dr Hybrid", 99, "Clinical Practice")
        self.assertEqual(Person.constructor_calls - before, 1)
        self.assertEqual(lecturer.role(), "Doctor and Lecturer")
        self.assertEqual(lecturer.module_name, "Clinical Practice")
        self.assertEqual(lecturer.fee(7), 50)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            ClinicClock(-1)
        with self.assertRaises(ValueError):
            ClinicClock(169)
        with self.assertRaises(ValueError):
            StudentPatient("", 10)
        with self.assertRaises(ValueError):
            Doctor("Bad ID", 0)

    def test_pending_appointment_can_be_cancelled(self):
        self.clinic.book(20, self.student, self.doctor, 15)
        self.clinic.cancel(20, "Patient changed plans")
        self.assertEqual(self.clinic.appointments[0].status, AppointmentStatus.CANCELLED)

    def test_appointment_ids_cannot_be_reused_after_cancellation(self):
        self.clinic.book(20, self.student, self.doctor, 15)
        self.clinic.cancel(20, "Patient changed plans")
        with self.assertRaises(ValueError):
            self.clinic.book(20, self.visitor, self.nurse, 16)


if __name__ == "__main__":
    unittest.main(verbosity=2)
