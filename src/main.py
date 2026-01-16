import os
import sys
from maze_validation import MazeValidator

def main():
    # Define the path to the required maze.json file
    maze_file = "maze.json"
    maze_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", maze_file))
    
    # Initialize the validator 
    validator = MazeValidator(maze_file)
    
    try:
        # Perform all mandatory checks
        # This will raise a ValueError if errors are present
        maze_data = validator.validate_all()
        
    except (FileNotFoundError, ValueError) as e:
        # Print the specific error message and terminate 
        print(f"VALIDATION ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"AN UNEXPECTED ERROR OCCURRED: {e}")
        sys.exit(1)

    # If we reach here, validation was successful.
    # Start the simulation phase.
    run_simulation(maze_data)

def run_simulation(maze):
    """simulation logic"""


if __name__ == "__main__":
    main()