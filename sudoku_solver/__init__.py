# Sudoku Solver Package
"""
A simple Sudoku solver with a Tkinter GUI.
"""

from .solver import solve_sudoku, is_valid, find_empty, find_all_solutions

__version__ = "2.0"
__all__ = ["solve_sudoku", "is_valid", "find_empty", "find_all_solutions"]
