### Constraints on Nurse-to-Room Assignment

def check_s2_minimum_skill_level(solution, data):
    """S2: Minimum Skill Level."""
    penalty = 0
    for nurse in solution['nurses']:
        for shift in nurse['assignments']:
            for room in shift['rooms']:
                for patient in solution['patients']:
                    if patient['room'] in room:
                        patient_data = next(p for p in data['patients'] if p['id'] == patient['id'])
                        required_skill = min(patient_data['skill_level_required'])
                        if nurse['skill_level'] < required_skill:
                            penalty += required_skill - nurse['skill_level']
    return penalty


def check_s3_continuity_of_care(solution, data):
    """S3: Continuity of Care."""
    penalty = 0
    for patient in solution['patients']:
        assigned_nurses = set()
        
        # Iterate over all days and shifts for the patient's stay
        for day in range(patient['admission_day'], patient['admission_day'] + patient['length_of_stay']):
            for nurse in solution['nurses']:
                for shift in nurse['assignments']:
                    if shift['day'] == day and patient['room'] in shift['rooms']:
                        assigned_nurses.add(nurse['id'])

        # Penalize if more than one nurse is assigned across the patient's stay
        penalty += len(assigned_nurses) - 1 if len(assigned_nurses) > 1 else 0

    return penalty

def check_s4_maximum_workload(solution, data):
    """
    Check and penalize violations of maximum workload for nurses.
    """
    penalty = 0
    for nurse in solution["nurses"]:
        for shift in nurse["assignments"]:
            # Calculate the total workload for this nurse and shift
            workload = sum(
                patient["surgery_duration"]
                for patient in solution["patients"]
                if patient["room"] in shift["rooms"]
                and patient["admission_day"] == shift["day"]
            )
            max_load = next(
                (
                    shift["max_load"]
                    for nurse_data in data["nurses"]
                    if nurse_data["id"] == nurse["id"]
                    for shift in nurse_data["working_shifts"]
                    if shift["day"] == shift["day"] and shift["shift"] == shift["shift"]
                ),
                None,
            )

            if max_load is not None and workload > max_load:
                penalty += workload - max_load  # Penalize the excess workload
    return penalty

