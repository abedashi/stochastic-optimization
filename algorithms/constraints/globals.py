### Global Constraints

def check_h5_mandatory_patients(solution, data):
    """H5: Mandatory Patients."""
    violations = len([
        patient for patient in data['patients']
        if patient['mandatory'] and patient['id'] not in [p['id'] for p in solution['patients']]
    ])
    return violations

def check_h6_admission_day(solution, data):
    """H6: Admission Day."""
    violations = 0
    for patient in solution['patients']:
        patient_data = next(p for p in data['patients'] if p['id'] == patient['id'])
        if patient['admission_day'] < patient_data['surgery_release_day']:
            violations += 1
    return violations

def check_s7_admission_delay(solution, data):
    """S7: Admission Delay."""
    delay = 0
    for patient in solution['patients']:
        patient_data = next(p for p in data['patients'] if p['id'] == patient['id'])
        delay += max(0, patient['admission_day'] - patient_data['surgery_release_day'])
    return delay

def check_s8_unscheduled_patients(solution, data):
    """S8: Unscheduled Patients."""
    unscheduled = len([
        patient for patient in data['patients']
        if not patient['mandatory'] and patient['id'] not in [p['id'] for p in solution['patients']]
    ])
    return unscheduled
