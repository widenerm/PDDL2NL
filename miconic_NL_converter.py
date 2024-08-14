import os
from tarski.io import PDDLReader
from tarski.syntax.formulas import Atom, CompoundFormula

# Define the path to your PDDL files
domain_file_path = ''
problems_directory = ''
output_directory = ''

# Load and parse PDDL files
def load_and_parse_pddl(domain_file, problem_file):
    reader = PDDLReader(raise_on_error=True)
    domain = reader.parse_domain(domain_file)
    problem = reader.parse_instance(problem_file)
    return domain, problem

# Convert PDDL objects and problem to natural language
def convert_to_narrative(domain, problem):
    narrative = []

    # Describe actions
    actions = [
        "Board: A passenger boards the lift at their origin floor.",
        "Depart: A passenger departs the lift at their destination floor.",
        "Move up: Move the lift from one floor to a higher floor.",
        "Move down: Move the lift from one floor to a lower floor."
    ]

    narrative.append("I am operating a lift system that transports passengers between different floors of a building. Here are the actions the lift can perform:")
    for action in actions:
        narrative.append(action)

    # Restrictions
    restrictions = [
        "Board: A passenger can only board the lift if the lift is at the same floor as the passenger's origin floor and the passenger is waiting at their origin floor.",
        "Depart: A passenger can only depart the lift if the lift is at the passenger's destination floor and the passenger is currently on the lift.",
        "Move up: The lift can only move up if it is currently at a floor and there is a floor above the current floor.",
        "Move down: The lift can only move down if it is currently at a floor and there is a floor below the current floor.",
        "Once a passenger boards the lift, they are no longer waiting at their origin floor and are now on the lift.",
        "Once a passenger departs the lift, they are no longer on the lift and have reached their destination floor."
    ]

    narrative.append("I have the following restrictions on the lift's actions:")
    for restriction in restrictions:
        narrative.append(restriction)

    # Initial state
    initial_state = problem.init.as_atoms()
    initial_conditions = []
    for atom in initial_state:
        predicate = atom.predicate.name
        args = [str(arg).lower() for arg in atom.subterms]
        if predicate == 'lift-at':
            initial_conditions.append(f"The lift is at floor {args[0]}.")
        elif predicate == 'origin':
            initial_conditions.append(f"Passenger {args[0]} is waiting at their origin floor {args[1]}.")
        elif predicate == 'destin':
            initial_conditions.append(f"Passenger {args[0]} has a destination floor {args[1]}.")
        elif predicate == 'passenger':
            initial_conditions.append(f"{args[0]} is a passenger.")
        elif predicate == 'floor':
            initial_conditions.append(f"{args[0]} is a floor.")
        elif predicate == 'above':
            initial_conditions.append(f"Floor {args[1]} is above floor {args[0]}.")
        else:
            initial_conditions.append(f"{predicate}({', '.join(args)})")

    narrative.append("As initial conditions, I have the following:")
    for condition in initial_conditions:
        narrative.append(condition)

    # Goal state
    goal_conditions = []
    if isinstance(problem.goal, Atom):
        goal_conditions.append(problem.goal)
    elif isinstance(problem.goal, CompoundFormula):
        goal_conditions.extend(problem.goal.subformulas)
    else:
        goal_conditions.append(problem.goal)

    narrative.append("My goal is to transport all passengers to their respective destination floors such that:")
    for g in goal_conditions:
        predicate = g.predicate.name
        args = [str(arg).lower() for arg in g.subterms]
        if predicate == 'served':
            narrative.append(f"Passenger {args[0]} is served.")
        else:
            narrative.append(f"{predicate}({', '.join(args)})")

    return "\n".join(narrative)

# Save the narrative description to a text file
def save_to_file(narrative, output_file):
    with open(output_file, 'w') as f:
        f.write(narrative)

# Process all problem files in the directory
def process_problem_files(domain_file, problems_directory, output_directory):
    for filename in os.listdir(problems_directory):
        if filename.endswith(".pddl") and filename != "domain.pddl":
            problem_file_path = os.path.join(problems_directory, filename)
            output_file_path = os.path.join(output_directory, filename.replace('.pddl', '_NL.txt'))

            domain, problem = load_and_parse_pddl(domain_file, problem_file_path)
            narrative = convert_to_narrative(domain, problem)
            save_to_file(narrative, output_file_path)
            print(f"Processed {filename}, output saved to {output_file_path}")

def main():
    process_problem_files(domain_file_path, problems_directory, output_directory)

if __name__ == "__main__":
    main()
