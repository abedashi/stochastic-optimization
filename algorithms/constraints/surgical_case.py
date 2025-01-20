### Constraints on Surgical Case Planning

def check_h3_surgeon_overtime(solution, data):
    """
    Check and penalize surgeon overtime violations.
    """
    violations = 0
    for surgeon in data['surgeons']:
        for day in range(data['days']):
            total_surgery_time = sum(
                patient['surgery_duration'] for patient in solution['patients']
                if patient['surgeon_id'] == surgeon['id'] and patient['admission_day'] == day
            )
            if total_surgery_time > surgeon['max_surgery_time'][day]:
                violations += (total_surgery_time - surgeon['max_surgery_time'][day])  # Penalize based on excess
    return violations

def check_h4_ot_overtime(solution, data):
    """H4: OT Overtime."""
    violations = 0
    for ot in data['operating_theaters']:
        for day in range(data['days']):
            total_time = sum(
                patient['surgery_duration'] for patient in solution['patients']
                if patient['operating_theater'] == ot['id'] and patient['admission_day'] == day
            )
            if total_time > ot['availability'][day]:
                violations += 1
    return violations


def check_s5_open_ots(solution, data):
    """S5: Open Operating Theaters."""
    penalty = 0
    for day in range(data['days']):
        open_ots = set(
            patient['operating_theater'] for patient in solution['patients']
            if patient['admission_day'] == day
        )
        penalty += len(open_ots)
    return penalty


def check_s6_surgeon_transfer(solution, data):
    """S6: Surgeon Transfer."""
    penalty = 0
    for surgeon in data['surgeons']:
        ot_ids = set(
            patient['operating_theater'] for patient in solution['patients']
            if patient['surgeon_id'] == surgeon['id']
        )
        penalty += len(ot_ids) - 1  # Minimize transfers between theaters
    return penalty
