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
        "Move: Move the robot from one room to another.",
        "Pick up a ball: Use the gripper to pick up a ball in the same room as the robot.",
        "Drop a ball: Use the gripper to drop a ball in the same room as the robot."
    ]

    narrative.append("I am managing a robot that needs to move balls between rooms using a gripper. Here are the actions the robot can perform:")
    for action in actions:
        narrative.append(action)

    # Restrictions
    restrictions = [
        "Move: The robot can only move between rooms if it is currently in one of the rooms.",
        "Pick up a ball: The robot can only pick up a ball if the ball is in the same room as the robot, the robot is in the room, and the gripper is free to hold the ball.",
        "Drop a ball: The robot can only drop a ball if the ball is currently being carried by the gripper and the robot is in the room where the ball is to be dropped.",
        "Once the robot picks up a ball, the ball is no longer in the room and the gripper is no longer free.",
        "Once the robot drops a ball, the ball is in the room and the gripper becomes free again."
    ]

    narrative.append("I have the following restrictions on the robot's actions:")
    for restriction in restrictions:
        narrative.append(restriction)

    # Initial state
    initial_state = problem.init.as_atoms()
    initial_conditions = []
    for atom in initial_state:
        predicate = atom.predicate.name
        args = [str(arg).lower() for arg in atom.subterms]
        if predicate == 'at-robby':
            initial_conditions.append(f"The robot is in room {args[0]}")
        elif predicate == 'at':
            initial_conditions.append(f"Ball {args[0]} is in room {args[1]}")
        elif predicate == 'free':
            initial_conditions.append(f"The {args[0]} gripper is free")
        elif predicate == 'ball':
            initial_conditions.append(f"{args[0]} is a ball")
        elif predicate == 'room':
            initial_conditions.append(f"{args[0]} is a room")
        elif predicate == 'gripper':
            initial_conditions.append(f"{args[0]} is a gripper")
        else:
            initial_conditions.append(f"{predicate}({', '.join(args)})")

    narrative.append("As initial conditions I have that:")
    for condition in initial_conditions:
        narrative.append(condition + ",")

    # Goal state
    goal_conditions = []
    if isinstance(problem.goal, Atom):
        goal_conditions.append(problem.goal)
    elif isinstance(problem.goal, CompoundFormula):
        goal_conditions.extend(problem.goal.subformulas)
    else:
        goal_conditions.append(problem.goal)

    narrative.append("My goal is to have that:")
    for g in goal_conditions:
        predicate = g.predicate.name
        args = [str(arg).lower() for arg in g.subterms]
        if predicate == 'at':
            narrative.append(f"Ball {args[0]} is in room {args[1]}")
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
