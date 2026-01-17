import json
import os

class MazeValidator:
    def __init__(self, file_path):
        self.file_path = file_path # json file path (where the maze is stored)
        self.maze = []
        self.rows = 0
        self.cols = 0

    def load_maze(self):
        """0) Loads the JSON file and parses the maze matrix."""

        # file existence check
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Error: {self.file_path} not found.")
        
        # load maze from JSON
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            self.maze = data.get("maze", [])
            
        if not self.maze:
            raise ValueError("Error: Maze is empty or format is invalid.")
        
        self.rows = len(self.maze)
        self.cols = len(self.maze[0]) # columns number based on first row

    def column_check(self):
        """1) Rows must have the same number of columns."""
        for i in range(len(self.maze)):
            row = self.maze[i]
            if len(row) != self.cols:
                raise ValueError(f"Error: Row {i} has {len(row)} columns, instead of {self.cols} expected.")

    def boundaries_check(self):
        """2) Perimeter must only contain walls (X), start (S), or end (E)."""
        allowed = {'X', 'S', 'E'}
        for r in range(self.rows):
            for c in range(self.cols):
                # Check if the cell is on the perimeter
                if r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1:
                    if self.maze[r][c] not in allowed:
                        raise ValueError(f"Error: Invalid character '{self.maze[r][c]}' on perimeter at ({r}, {c}).")

    def start_end_presence_check(self):
        """3) Both start and end must be present."""
        flat_maze = [cell for row in self.maze for cell in row]
        if 'S' not in flat_maze:
            raise ValueError("Error: Start ('S') not found in maze.")
        if 'E' not in flat_maze:
            raise ValueError("Error: End ('E') not found in maze.")

    def unitary_start_end_check(self):
        """4) There must be exactly one start and one end."""
        flat_maze = [cell for row in self.maze for cell in row]
        if flat_maze.count('S') != 1:
            raise ValueError("Error: There must be exactly one start ('S').")
        if flat_maze.count('E') != 1:
            raise ValueError("Error: There must be exactly one end ('E').")

    def feasibility_check(self):
        """5) Start and end must be on the maze perimeter."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c] in ('S', 'E'):
                    is_on_perimeter = (r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1)
                    if not is_on_perimeter:
                        raise ValueError(f"Error: '{self.maze[r][c]}' must be on the perimeter.")

    def validate_all(self):
        """Runs all checks in sequence (this is the only method that should be called externally)."""
        self.load_maze()
        self.column_check()
        self.boundaries_check()
        self.start_end_presence_check()
        self.unitary_start_end_check()
        self.feasibility_check()
        print("Maze validation successful.")
        return self.maze # return maze data for further processing