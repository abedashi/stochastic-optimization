from .constraints.patient_admission import check_h1_gender_mix, check_h2_compatible_rooms, check_s1_age_groups, check_h7_room_capacity, check_uncovered_rooms
from .constraints.nurse_to_room import check_s2_minimum_skill_level, check_s3_continuity_of_care, check_s4_maximum_workload
from .constraints.surgical_case import check_h3_surgeon_overtime, check_h4_ot_overtime, check_s5_open_ots, check_s6_surgeon_transfer
from .constraints.globals import check_h5_mandatory_patients, check_h6_admission_day, check_s7_admission_delay, check_s8_unscheduled_patients

def calculate_cost(solution, data):
    """Calculate the total cost of the solution, including hard and soft constraints."""
    total_cost = 0

    # HARD CONSTRAINT PENALTIES
    penalty_hard = 0

    # Patient Admission Scheduling Constraints
    penalty_hard += check_h1_gender_mix(solution, data) * 1000  # H1: No gender mix
    penalty_hard += check_h2_compatible_rooms(solution, data)  # H2: Compatible rooms
    penalty_hard += check_h7_room_capacity(solution, data) * 1000  # H7: Room capacity
    penalty_hard += check_h5_mandatory_patients(solution, data)  # H5: Mandatory patients
    penalty_hard += check_uncovered_rooms(solution, data)

    # Surgical Case Planning Constraints
    penalty_hard += check_h3_surgeon_overtime(solution, data) * 5000  # H3: Surgeon overtime
    penalty_hard += check_h4_ot_overtime(solution, data) * 5000 # H4: OT overtime
    penalty_hard += check_h6_admission_day(solution, data)  # H6: Admission day

    # Nurse-to-Room Assignment Constraints

    total_cost += penalty_hard

    # SOFT CONSTRAINT PENALTIES
    penalty_soft = 0

    # Patient Admission Scheduling Constraints
    penalty_soft += check_s1_age_groups(solution, data) * data['weights'].get('room_mixed_age')  # S1: Age groups

    # Nurse-to-Room Assignment Constraints
    penalty_hard += check_s4_maximum_workload(solution, data) * data['weights'].get('nurse_eccessive_workload')  # S4: Maximum workload
    penalty_soft += check_s2_minimum_skill_level(solution, data) * data['weights'].get('room_nurse_skill')  # S2: Minimum skill level
    penalty_soft += check_s3_continuity_of_care(solution, data) * data['weights'].get('continuity_of_care')  # S3: Continuity of care

    # Surgical Case Planning Constraints
    penalty_soft += check_s5_open_ots(solution, data) * data['weights'].get('open_operating_theater')  # S5: Open OTs
    penalty_soft += check_s6_surgeon_transfer(solution, data) * data['weights'].get('surgeon_transfer')  # S6: Surgeon transfer

    # Global Constraints
    penalty_soft += check_s7_admission_delay(solution, data) * data['weights'].get('patient_delay')  # S7: Admission delay
    penalty_soft += check_s8_unscheduled_patients(solution, data) * data['weights'].get('unscheduled_optional')  # S8: Unscheduled patients

    total_cost += penalty_soft

    return total_cost