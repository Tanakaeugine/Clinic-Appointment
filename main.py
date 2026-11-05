
from clock import ClinicClock
from logger import AppointmentLogger
from clinic import Clinic
from patient import StudentPatient, StaffMemberPatient, VisitorPatient
from staff import Doctor, Nurse, Pharmacist, MedicalLecturer
from person import Person


P = 7


def main():
    clock = ClinicClock(8)
    with AppointmentLogger("clinic.log") as journal:
        clinic = Clinic(clock, journal, P)

        print("\\n--- PATIENT REGISTRATION ---")
        patients = [
            StudentPatient("John", 101),
            StaffMemberPatient("Peter", 102),
            VisitorPatient("Sarah", 103),
        ]
        for patient in patients:
            clinic.register_patient(patient)

        print("\\n--- MULTIPLE INHERITANCE ---")
        before = Person.constructor_calls
        medical_lecturer = MedicalLecturer("Dr Brown", 204, "Clinical Practice")
        print(f"Person constructor calls for MedicalLecturer: {Person.constructor_calls - before}")
        print(f"Teaching module: {medical_lecturer.module_name}")

        print("\\n--- STAFF REGISTRATION ---")
        staff = [
            Doctor("Dr Smith", 201),
            Nurse("Mary", 202),
            Pharmacist("James", 203),
            medical_lecturer,
        ]
        for member in staff:
            clinic.register_staff(member)

        print("\\n--- POLYMORPHIC FEE SCHEDULE ---")
        for member in clinic.staff_members:
            print(f"{member.name}: {member.role()} - ${member.fee(P):g}")

        print("\\n--- BOOKING AND DISCOUNTS ---")
        bookings = [
            (301, patients[0], staff[0], 15),
            (302, patients[1], staff[1], 20),
            (303, patients[2], staff[2], 25),
            (304, patients[0], staff[3], 30),
        ]
        for appointment_id, patient, member, hour in bookings:
            clinic.book(appointment_id, patient, member, hour)

        clinic.confirm(301)
        for appointment in clinic.appointments:
            print(
                f"{appointment.patient.name} ({appointment.patient.patient_category()}): "
                f"${clinic.fee_for(appointment.appointment_id):g}"
            )

        print("\\n--- CANCELLATION ---")
        clinic.cancel(302, "Patient requested cancellation")

        print("\\n--- DELIBERATE FAILURE: DOUBLE BOOKING ---")
        try:
            clinic.book(305, patients[0], staff[2], 15)
        except ValueError as error:
            print(f"Booking correctly rejected: {error}")

        print("\\n--- APPOINTMENT REGISTER ---")
        for appointment in clinic.appointments:
            print(
                f"#{appointment.appointment_id} | {appointment.patient.name} | "
                f"{appointment.staff.name} | hour {appointment.start_hour} | "
                f"{appointment.status.value}"
            )


if __name__ == "__main__":
    main()
