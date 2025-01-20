from .patient_admission import check_h1_gender_mix, check_h2_compatible_rooms, check_h7_room_capacity, check_uncovered_rooms
from .surgical_case import check_h3_surgeon_overtime, check_h4_ot_overtime
from .globals import check_h5_mandatory_patients, check_h6_admission_day

def count_hard_violations(solution, data):
    violations = 0

    # Check H1: No Gender Mix
    violations += check_h1_gender_mix(solution, data)

    # Check H2: Room Compatibility
    violations += check_h2_compatible_rooms(solution, data)

    # Check H7: Room Capacity
    violations += check_h7_room_capacity(solution, data)

    # Check H3: Surgeon Overtime
    violations += check_h3_surgeon_overtime(solution, data)

    # Check H4: OT Overtime
    violations += check_h4_ot_overtime(solution, data)

    # Check H5: Mandatory Patients
    violations += check_h5_mandatory_patients(solution, data)

    # Check H6: Admission Day
    violations += check_h6_admission_day(solution, data)

    violations += check_uncovered_rooms(solution, data)

    return violations
