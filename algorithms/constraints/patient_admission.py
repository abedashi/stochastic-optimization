### Constraints on Patient Admission Scheduling

def check_h1_gender_mix(solution, data):
    """H1: No Gender Mix."""
    violations = 0
    for room in data['rooms']:
        for day in range(data['days']):
            genders = [
                patient['gender'] for patient in solution['patients']
                if patient['room'] == room['id'] and patient['admission_day'] <= day < patient['admission_day'] + patient['length_of_stay']
            ]
            if len(set(genders)) > 1:
                violations += 1
    return violations


def check_h2_compatible_rooms(solution, data):
    """H2: Compatible Rooms."""
    violations = 0
    for patient in solution['patients']:
        patient_data = next(p for p in data['patients'] if p['id'] == patient['id'])
        if patient['room'] in patient_data.get('incompatible_room_ids', []):
            violations += 1
    return violations

def check_s1_age_groups(solution, data):
    """
    Check and penalize age group differences in shared rooms (S1).
    """
    penalty = 0
    AGE_GROUP_MAPPING = {
        "infant": 1,
        "adult": 2,
        "elderly": 3
    }
    for room in data['rooms']:
        for day in range(data['days']):
            ages = [
                AGE_GROUP_MAPPING[patient['age_group']] for patient in solution['patients']
                if patient['room'] == room['id'] and patient['admission_day'] <= day < patient['admission_day'] + patient['length_of_stay']
            ]
            if ages:
                penalty += max(ages) - min(ages)  # Calculate the age difference
    return penalty


def check_h7_room_capacity(solution, data):
    """H7: Room Capacity."""
    violations = 0
    for room in data['rooms']:
        for day in range(data['days']):
            occupancy = sum(
                1 for patient in solution['patients']
                if patient['room'] == room['id'] and patient['admission_day'] <= day < patient['admission_day'] + patient['length_of_stay']
            )
            if occupancy > room['capacity']:
                violations += 1
    return violations

def check_uncovered_rooms(solution, data):
    """
    Check for uncovered rooms. A room is considered uncovered if it has patients 
    but no nurses assigned for any of its shifts on a given day.
    """
    violations = 0

    for room in data['rooms']:
        for day in range(data['days']):
            # Check if the room has patients on this day
            has_patients = any(
                patient['room'] == room['id'] and patient['admission_day'] <= day < patient['admission_day'] + patient['length_of_stay']
                for patient in solution['patients']
            )
            if has_patients:
                # Check if there is at least one nurse assigned for each shift
                for dataNurse in data['nurses']:
                    for workingShift in dataNurse['working_shifts']:
                        has_nurse = any(
                            room['id'] in assignment['rooms'] and assignment['day'] == day and assignment['shift'] == workingShift["shift"]
                            for nurse in solution['nurses']
                            for assignment in nurse['assignments']
                        )
                        if not has_nurse:
                            violations += 1
    return violations