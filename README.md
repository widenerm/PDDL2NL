# pddl2nl

This repository contains code and data for converting Planning Domain Definition Language (PDDL) files into natural language (NL) descriptions. The project includes Python scripts for conversion, training problems in NL, and test problems generated and converted using various tools.

## Repository Structure
- [**blocks_NL_converter.py**](https://github.com/widenerm/pddl2nl/blob/main/blocks_NL_converter.py): Python script for converting blocksworld PDDL problem files to natural language prompts.
- [**driverlog_NL_converter.py**](https://github.com/widenerm/pddl2nl/blob/main/driverlog_NL_converter.py): Python script for converting driverlog PDDL problem files to natural language prompts.
- [**gripper_NL_converter.py**]([https://github.com/widenerm/pddl2nl/blob/main/gripper_NL_converter.py): Python script for converting gripper PDDL problem files to natural language prompts.
- [**miconic_NL_converter.py**](https://github.com/widenerm/pddl2nl/blob/main/miconic_NL_converter.py): Python script for converting miconic PDDL problem files to natural language prompts.
- [**movie_NL_converter.py**](https://github.com/widenerm/pddl2nl/blob/main/movie_NL_converter.py): Python script for converting movie PDDL problem files to natural language prompts.

## Training Problems
- **train_NL_problems.txt.zip** contains natural language prompts converted from [downward-benchmarks](https://github.com/aibasel/downward-benchmarks/tree/master) in the five domains listed above using their corresponding script.

## Test Problems
- **test_NL_problems.txt.zip** contains natural language prompts converted from problems generated by [pddl generators](https://github.com/AI-Planning/pddl-generators) in the five domains listed above using their corresponding script.
