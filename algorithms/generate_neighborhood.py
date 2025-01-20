import copy

def generate_neighborhood(solution, data):
    """Generate neighborhood focusing on reducing SurgeonOvertime, TheaterOvertime, and GenderMix."""
    neighbors = []

    for i, patient in enumerate(solution['patients']):
        # Get the patient data
        patient_data = next(p for p in data['patients'] if p['id'] == patient['id'])

        # Modify surgery schedule (day)
        for new_day in range(patient_data['surgery_release_day'], data['days']):
            total_surgery_time = sum(
                p['surgery_duration'] for p in solution['patients']
                if p['surgeon_id'] == patient['surgeon_id'] and p['admission_day'] == new_day
            )
            max_time = next(s['max_surgery_time'][new_day] for s in data['surgeons'] if s['id'] == patient['surgeon_id'])
            if total_surgery_time + patient['surgery_duration'] <= max_time:
                new_solution = copy.deepcopy(solution)
                new_solution['patients'][i]['admission_day'] = new_day
                neighbors.append(new_solution)

        # Reassign surgeon
        for surgeon in data['surgeons']:
            if surgeon['id'] != patient['surgeon_id']:
                if patient['surgery_duration'] <= surgeon['max_surgery_time'][patient['admission_day']]:
                    new_solution = copy.deepcopy(solution)
                    new_solution['patients'][i]['surgeon_id'] = surgeon['id']
                    neighbors.append(new_solution)

        # Reassign operating theater
        for theater in data['operating_theaters']:
            if theater['id'] != patient['operating_theater']:
                total_theater_time = sum(
                    p['surgery_duration'] for p in solution['patients']
                    if p['operating_theater'] == theater['id'] and p['admission_day'] == patient['admission_day']
                )
                if total_theater_time + patient['surgery_duration'] <= theater['availability'][patient['admission_day']]:
                    new_solution = copy.deepcopy(solution)
                    new_solution['patients'][i]['operating_theater'] = theater['id']
                    neighbors.append(new_solution)

        # Reduce gender mix violations
        for room in data['rooms']:
            if room['id'] != patient['room']:
                is_gender_compatible = all(
                    p['gender'] == patient['gender'] for p in solution['patients']
                    if p['room'] == room['id'] and
                       p['admission_day'] <= patient['admission_day'] < p['admission_day'] + p['length_of_stay']
                )
                if is_gender_compatible:
                    new_solution = copy.deepcopy(solution)
                    new_solution['patients'][i]['room'] = room['id']
                    neighbors.append(new_solution)

        # Reduce uncovered room violations
        for nurse in solution['nurses']:
            for shift in nurse['assignments']:
                if patient['admission_day'] <= shift['day'] < patient['admission_day'] + patient['length_of_stay']:
                    if patient['room'] not in shift['rooms']:
                        new_solution = copy.deepcopy(solution)
                        nurse_idx = next(n_idx for n_idx, n in enumerate(new_solution['nurses']) if n['id'] == nurse['id'])
                        new_solution['nurses'][nurse_idx]['assignments'].append({
                            "day": shift['day'],
                            "shift": shift['shift'],
                            "rooms": list(set(shift['rooms'] + [patient['room']]))
                        })
                        neighbors.append(new_solution)

    return neighbors