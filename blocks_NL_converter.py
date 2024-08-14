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
        "Pick up a block",
        "Put down a block",
        "Stack a block on top of another block",
        "Unstack a block from on top of another block"
    ]

    narrative.append("I am playing with a set of blocks where I need to arrange the blocks into stacks. Here are the actions I can do:")
    for action in actions:
        narrative.append(action)

    # Restrictions
    restrictions = [
        "I can only pick up or unstack one block at a time.",
        "I can only pick up or unstack a block if my hand is empty.",
        "I can only pick up a block if the block is on the table and the block is clear. A block is clear if the block has no other blocks on top of it and if the block is not picked up.",
        "I can only unstack a block from on top of another block if the block I am unstacking was really on top of the other block.",
        "I can only unstack a block from on top of another block if the block I am unstacking is clear.",
        "Once I pick up or unstack a block, I am holding the block.",
        "I can only put down a block that I am holding.",
        "I can only stack a block on top of another block if I am holding the block being stacked.",
        "I can only stack a block on top of another block if the block onto which I am stacking the block is clear.",
        "Once I put down or stack a block, my hand becomes empty.",
        "Once you stack a block on top of a second block, the second block is no longer clear."
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
        if predicate == 'clear':
            initial_conditions.append(f"block {args[0]} is clear")
        elif predicate == 'ontable':
            initial_conditions.append(f"block {args[0]} is on the table")
        elif predicate == 'handempty':
            initial_conditions.append("my hand is empty")
        elif predicate == 'on':
            initial_conditions.append(f"block {args[0]} is on block {args[1]}")
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
        if predicate == 'on':
            goal_conditions.append(f"block {args[0]} is on block {args[1]}")
        elif predicate == 'clear':
            goal_conditions.append(f"block {args[0]} is clear")
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
