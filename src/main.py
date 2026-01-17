import os
import sys
import time
from maze_validation import MazeValidator
from maze_logic import MazeSimulator


def main():
    # Define the path to the required maze.json file
    maze_file = "maze.json"
    maze_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", maze_file))
    
    # Initialize the validator 
    validator = MazeValidator(maze_file)
    
    try:
        # Perform all mandatory checks for the maze
        # check for file existence, format, boundaries, start/end presence and uniqueness, feasibility
        maze_data = validator.validate_all()
        
    except (FileNotFoundError, ValueError) as e:
        # Print the specific error message and terminate 
        print(f"VALIDATION ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"AN UNEXPECTED ERROR OCCURRED: {e}")
        sys.exit(1) # a general unexpected error occurred

    # If we reach here, validation was successful.
    # Now the simulation phase starts.

    time.sleep(3)
    print("\n--- Starting Simulation ---")
    simulator = MazeSimulator(maze_data)
    simulator.start_simulation()




if __name__ == "__main__":
    main()