import random

def generate_initial_solution(data):
    """Generate an initial solution prioritizing mandatory patients."""
    solution = {"patients": [], "nurses": []}
    room_occupancy = {room['id']: [0] * data['days'] for room in data['rooms']}

    # Assign mandatory patients first
    for patient in data['patients']:
        if patient['mandatory']:
            for day in range(patient['surgery_release_day'], data['days'] - patient['length_of_stay'] + 1):
                assigned_room = next(
                    (room for room in data['rooms']
                     if all(room_occupancy[room['id']][d] < room['capacity']
                            for d in range(day, day + patient['length_of_stay']))),
                    None
                )
                if assigned_room:
                    for d in range(day, day + patient['length_of_stay']):
                        room_occupancy[assigned_room['id']][d] += 1
                    solution['patients'].append({
                        "id": patient['id'],
                        "admission_day": day,
                        "room": assigned_room['id'],
                        "operating_theater": random.choice(data['operating_theaters'])['id'],
                        "age_group": patient['age_group'],
                        "gender": patient['gender'],
                        "length_of_stay": patient['length_of_stay'],
                        "surgeon_id": patient['surgeon_id'],
                        "surgery_duration": patient['surgery_duration']
                    })
                    break

    # Assign non-mandatory patients as much as possible
    for patient in data['patients']:
        if not patient['mandatory']:
            for day in range(patient['surgery_release_day'], data['days'] - patient['length_of_stay'] + 1):
                assigned_room = next(
                    (room for room in data['rooms']
                     if all(room_occupancy[room['id']][d] < room['capacity']
                            for d in range(day, day + patient['length_of_stay']))),
                    None
                )
                if assigned_room:
                    for d in range(day, day + patient['length_of_stay']):
                        room_occupancy[assigned_room['id']][d] += 1
                    solution['patients'].append({
                        "id": patient['id'],
                        "admission_day": day,
                        "room": assigned_room['id'],
                        "operating_theater": random.choice(data['operating_theaters'])['id'],
                        "age_group": patient['age_group'],
                        "gender": patient['gender'],
                        "length_of_stay": patient['length_of_stay'],
                        "surgeon_id": patient['surgeon_id'],
                        "surgery_duration": patient['surgery_duration']
                    })
                    break

    # Assign nurses with metadata (skill_level)
    for nurse in data['nurses']:
        assignments = []
        for shift in nurse['working_shifts']:
            rooms = random.sample([room['id'] for room in data['rooms']], random.randint(1, len(data['rooms'])))
            assignments.append({"day": shift['day'], "shift": shift['shift'], "rooms": rooms})

        solution['nurses'].append({
            "id": nurse['id'],
            "skill_level": nurse['skill_level'],
            "assignments": assignments
        })

    return solution