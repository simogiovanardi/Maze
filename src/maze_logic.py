import time
import os
import sys

class MazeSimulator:
    def __init__(self, maze_layout):
        self.maze = maze_layout
        self.rows = len(maze_layout)
        self.cols = len(maze_layout[0])
        self.person_pos = None
        self.start_pos = None
        self.end_pos = None
        # Directions: 0: North, 1: East, 2: South, 3: West
        self.current_direction = 1 # Start facing East by default
        self.is_running = True

        # Find start and end positions
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c] == 'S':
                    self.start_pos = (r, c)
                    self.person_pos = [r, c] # Assign person position to start
                elif self.maze[r][c] == 'E':
                    self.end_pos = (r, c)

    def print_maze(self):
        """Prints maze and the person (current state)."""

        os.system('cls' if os.name == 'nt' else 'clear') # Clear console
        
        for r in range(self.rows):
            row_str = ""
            for c in range(self.cols):
                if r == self.person_pos[0] and c == self.person_pos[1]:
                    row_str += "P " # 'P' represents the Person
                else:
                    row_str += f"{self.maze[r][c]} "
            print(row_str)

    def first_step(self):
        """First turn only: Place person at start position and wait."""
        print("Positioning person at start...")
        time.sleep(3)
        self.print_maze()
        time.sleep(1)

    def get_move_coordinates(self, direction):
        """Logic to find the next step (right side) based on current direction of the person."""
        r, c = self.person_pos
        if direction == 0: return r - 1, c # next cell, if person direction is North
        if direction == 1: return r, c + 1 # East
        if direction == 2: return r + 1, c # South
        if direction == 3: return r, c - 1 # West
        return r, c

    def move_person(self):
        """
        Moves the person one cell using the Right-Hand Rule.
        Logic:
            Try to turn Right, but if blocked by a wall, go Straight.
            If still blocked, turn Left. If all three are blocked, turn Back.
        """
        # Right-Hand Rule: 
        # 1. Turn Right, based on person current direction
        # 2. Go Straight
        # 3. Turn Left
        # 4. Turn Around
        
        priorities = [
            (self.current_direction + 1) % 4, # Right
            self.current_direction,           # Straight
            (self.current_direction - 1) % 4, # Left
            (self.current_direction + 2) % 4  # Back
        ]

        for d in priorities:
            new_r, new_c = self.get_move_coordinates(d)
            # Check if move is valid (not a wall 'X')
            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                if self.maze[new_r][new_c] != 'X':
                    self.person_pos = [new_r, new_c]
                    self.current_direction = d
                    break

    def check_result(self):
        """Verifies if the person reached the exit or returned to start."""
        current_cell = self.maze[self.person_pos[0]][self.person_pos[1]]
        
        if current_cell == 'E':
            self.print_maze()
            print("SUCCESS: The person found the exit! ")
            self.is_running = False
        elif current_cell == 'S':
            self.print_maze()
            print("FAILURE: No valid path found. Returned to start.")
            self.is_running = False

    def run_turn(self):
        """Executes a single turn logic."""
        self.move_person()
        self.print_maze()
        self.check_result()
        if self.is_running:
            time.sleep(1)

    def start_simulation(self):
        """Main loop for the entire simulation."""
        self.first_step()
        while self.is_running:
            self.run_turn()