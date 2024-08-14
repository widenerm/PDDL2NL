import os
from tarski.io import PDDLReader

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
        "Load an object onto a truck",
        "Unload an object from a truck",
        "Board a driver onto a truck",
        "Disembark a driver from a truck",
        "Drive a truck from one location to another",
        "Walk a driver from one location to another"
    ]

    narrative.append("I am managing a logistics operation where I need to transport goods and drivers between locations using trucks. Here are the actions I can do:")
    for action in actions:
        narrative.append(action)

    # Restrictions
    restrictions = [
        "I can only load an object onto a truck if both the object and the truck are at the same location.",
        "I can only unload an object from a truck if both the object and the truck are at the same location.",
        "I can only board a driver onto a truck if the truck is at the same location as the driver and the truck is empty.",
        "I can only disembark a driver from a truck if the truck is at the same location as the driver.",
        "I can only drive a truck from one location to another if the truck is at the starting location, a driver is already boarded onto the truck, and there is a direct link between the two locations.",
        "I can only walk a driver from one location to another if the driver is at the starting location and there is a path between the two locations.",
        "Once an object is loaded onto a truck, it is no longer at the original location.",
        "Once an object is unloaded from a truck, it is at the new location.",
        "Once a driver boards a truck, they are no longer at the original location, and the truck is no longer empty.",
        "Once a driver disembarks from a truck, they are at the new location, and the truck becomes empty.",
        "Once a truck is driven from one location to another, it is no longer at the original location but at the new location.",
        "Once a driver walks from one location to another, they are no longer at the original location but at the new location."
    ]

    narrative.append("I have the following restrictions on my actions:")
    for restriction in restrictions:
        narrative.append(restriction)

    # Initial state
    initial_state = problem.init.as_atoms()
    initial_conditions = []
    for atom in initial_state:
        predicate = atom.predicate.name
        args = [str(arg).lower() for arg in atom.subterms]
        if predicate == 'at':
            initial_conditions.append(f"{args[0]} is at {args[1]}")
        elif predicate == 'empty':
            initial_conditions.append(f"{args[0]} is empty")
        elif predicate == 'link':
            initial_conditions.append(f"there is a drivable link between {args[0]} and {args[1]}")
        elif predicate == 'path':
            initial_conditions.append(f"there is a walking path between {args[0]} and {args[1]}")
        elif predicate == 'driver':
            initial_conditions.append(f"{args[0]} is a driver")
        elif predicate == 'truck':
            initial_conditions.append(f"{args[0]} is a truck")
        elif predicate == 'obj':
            initial_conditions.append(f"{args[0]} is an object")
        elif predicate == 'location':
            initial_conditions.append(f"{args[0]} is a location")
        else:
            initial_conditions.append(f"{predicate}({', '.join(args)})")

    narrative.append("As initial conditions I have that,")
    for condition in initial_conditions:
        narrative.append(condition + ",")

    # Goal state
    goal_conditions = []
    for g in problem.goal.subformulas:
        predicate = g.predicate.name
        args = [str(arg).lower() for arg in g.subterms]
        if predicate == 'at':
            goal_conditions.append(f"{args[0]} is at {args[1]}")
        else:
            goal_conditions.append(f"{predicate}({', '.join(args)})")

    narrative.append("My goal is to have that:")
    for condition in goal_conditions:
        narrative.append(f"{condition}.")

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
