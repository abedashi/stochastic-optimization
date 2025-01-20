import json

def read_input(file_path):
    """Read input JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def write_solution(file_path, solution):
    """Write solution to JSON file."""
    with open(file_path, 'w') as f:
        json.dump(solution, f, indent=4)

def get_empty_solution():
    """Initialize an empty solution template."""
    return {"patients": [], "nurses": []}
