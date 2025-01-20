# tabu_search.py

import copy
from .initial_solution import generate_initial_solution
from .generate_neighborhood import generate_neighborhood
from .calculate_cost import calculate_cost

def tabu_search(data, iterations=50, tabu_tenure=10):
    """Tabu Search for optimizing the solution."""
    # Generate the initial solution
    current_solution = generate_initial_solution(data)
    best_solution = copy.deepcopy(current_solution)
    tabu_list = []  # List to store tabu solutions
    cost_history = []  # History of costs for tracking performance

    for it in range(iterations):
        # Generate a neighborhood of solutions
        neighborhood = generate_neighborhood(current_solution, data)
        
        # Select the best candidate not in the tabu list
        candidate_solution = min(
            neighborhood, 
            key=lambda sol: calculate_cost(sol, data)
        )
        
        # If the candidate improves the best solution, update it
        if calculate_cost(candidate_solution, data) < calculate_cost(best_solution, data):
            best_solution = copy.deepcopy(candidate_solution)

        # Update the current solution and maintain the tabu list
        current_solution = candidate_solution
        tabu_list.append(candidate_solution)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

        # Track cost history
        current_cost = calculate_cost(current_solution, data)
        cost_history.append(current_cost)

        print(f"Iteration {it}: Cost = {current_cost}")

    return best_solution, cost_history