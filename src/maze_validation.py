import json
import os


class MazeValidator:
    def __init__(self, file_path):
        self.file_path = file_path # 
        self.maze = []
        self.rows = 0
        self.cols = 0

    def load_maze(self):
        """Loads the JSON file and parses the maze matrix[cite: 14]."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Error: {self.file_path} not found.")
        
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            self.maze = data.get("maze", [])
            
        if not self.maze:
            raise ValueError("Error: Maze is empty or format is invalid.")
        
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])

    def column_check(self):
        """1) All rows must have the same number of columns[cite: 31]."""
        for i, row in enumerate(self.maze):
            if len(row) != self.cols:
                raise ValueError(f"Error: Row {i} has {len(row)} columns, expected {self.cols}[cite: 31].")

    def boundaries_check(self):
        """2) Perimeter must only contain walls (X), start (S), or end (E)[cite: 40]."""
        allowed = {'X', 'S', 'E'}
        for r in range(self.rows):
            for c in range(self.cols):
                # Check if the cell is on the perimeter
                if r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1:
                    if self.maze[r][c] not in allowed:
                        raise ValueError(f"Error: Invalid character '{self.maze[r][c]}' on perimeter at ({r}, {c})[cite: 40].")

    def start_end_presence_check(self):
        """3) Both start and end must be present[cite: 42]."""
        flat_maze = [cell for row in self.maze for cell in row]
        if 'S' not in flat_maze:
            raise ValueError("Error: Start ('S') not found in maze[cite: 42].")
        if 'E' not in flat_maze:
            raise ValueError("Error: End ('E') not found in maze[cite: 42].")

    def unitary_start_end_check(self):
        """4) There must be exactly one start and one end[cite: 44]."""
        flat_maze = [cell for row in self.maze for cell in row]
        if flat_maze.count('S') != 1:
            raise ValueError("Error: There must be exactly one start ('S')[cite: 44].")
        if flat_maze.count('E') != 1:
            raise ValueError("Error: There must be exactly one end ('E')[cite: 44].")

    def feasibility_check(self):
        """5) Start and end must be on the perimeter."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c] in ('S', 'E'):
                    is_on_perimeter = (r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1)
                    if not is_on_perimeter:
                        raise ValueError(f"Error: '{self.maze[r][c]}' must be on the perimeter.")

    def validate_all(self):
        """Runs all checks in sequence as required."""
        self.load_maze()
        self.column_check()
        self.boundaries_check()
        self.start_end_presence_check()
        self.unitary_start_end_check()
        self.feasibility_check()
        print("Maze validation successful.")
        return self.maze