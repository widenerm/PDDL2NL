import os
from tarski.io import PDDLReader
from tarski.syntax.formulas import Atom

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
        "Commit a resource: Attach a resource to an assembly.",
        "Release a resource: Detach a resource from an assembly.",
        "Assemble a part: Incorporate a part into an assembly.",
        "Remove a part: Take a part out of an assembly."
    ]

    narrative.append("I am working on assembling various parts to complete an assembly task. Here are the actions I can perform:")
    for action in actions:
        narrative.append(action)

    # Restrictions
    restrictions = [
        "I can only commit a resource if it is available. Once I commit a resource, it is no longer available.",
        "I can only release a resource if it is currently committed to an assembly. Once I release a resource, it becomes available again.",
        "I can only assemble a part if all required resources for the assembly are committed, the part is available, and all previous parts that need to be assembled before this part are already included.",
        "I can only remove a part if all required resources for the assembly are committed, the part is incorporated into the assembly, and the part is either a transient part or is the last part added.",
        "Once I assemble a part, it is incorporated into the assembly and is no longer available. If all parts are correctly assembled, the assembly is complete."
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
        if predicate == 'available':
            initial_conditions.append(f"Resource {args[0]} is available")
        elif predicate == 'requires':
            initial_conditions.append(f"Part {args[0]} requires resource {args[1]}")
        elif predicate == 'part-of':
            initial_conditions.append(f"Part {args[0]} is part of assembly {args[1]}")
        elif predicate == 'transient-part':
            initial_conditions.append(f"Part {args[0]} is a transient part of assembly {args[1]}")
        elif predicate == 'assemble-order':
            initial_conditions.append(f"Part {args[0]} should be assembled before part {args[1]}")
        elif predicate == 'remove-order':
            initial_conditions.append(f"Part {args[0]} should be removed before part {args[1]}")
        else:
            initial_conditions.append(f"{predicate}({', '.join(args)})")

    narrative.append("As initial conditions I have that,")
    for condition in initial_conditions:
        narrative.append(condition + ",")

    # Goal state
    goal_conditions = []
    if isinstance(problem.goal, Atom):
        goal_conditions.append(problem.goal)

    else:
        goal_conditions.append(problem.goal)

    narrative.append("My goal is to have that:")
    for g in goal_conditions:
        predicate = g.predicate.name
        args = [str(arg).lower() for arg in g.subterms]
        if predicate == 'complete':
            narrative.append(f"The assembly {args[0]} is complete")
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
