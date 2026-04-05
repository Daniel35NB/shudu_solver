# -*- coding: utf-8 -*-
"""
Sudoku GUI Module

This module contains the Tkinter-based graphical user interface for the Sudoku solver.
"""

import tkinter as tk
from tkinter import messagebox
from typing import List, Optional

from .solver import solve_sudoku, find_all_solutions


class SudokuGUI:
    """Graphical User Interface for the Sudoku Solver."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the Sudoku GUI.
        
        Args:
            root: The Tkinter root window.
        """
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.config(bg="#F5F5DC")
        
        self.sudoku_entries: List[List[tk.Entry]] = []
        self.solutions: List[List[List[int]]] = []
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Create sudoku grid frame
        sudoku_frame = tk.Frame(self.root, bg="#F5F5DC")
        sudoku_frame.pack(padx=10, pady=10)
        
        # Create 9x9 grid of entry widgets
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = tk.Entry(
                    sudoku_frame,
                    width=2,
                    font=("Arial", 16),
                    justify="center",
                    bg="#F5F5DC"
                )
                entry.grid(row=i, column=j, padx=1, pady=1)
                
                # Add thicker borders for 3x3 boxes
                if j % 3 == 0 and j != 0:
                    entry.grid_configure(padx=(5, 1))
                if i % 3 == 0 and i != 0:
                    entry.grid_configure(pady=(5, 1))
                
                row_entries.append(entry)
            self.sudoku_entries.append(row_entries)
        
        # Create buttons frame
        button_frame = tk.Frame(self.root, bg="#F5F5DC")
        button_frame.pack(pady=10)
        
        # Solve button
        solve_button = tk.Button(
            button_frame,
            text="Solve",
            command=self.solve,
            width=10
        )
        solve_button.pack(side=tk.LEFT, padx=5)
        
        # More button
        more_button = tk.Button(
            button_frame,
            text="More",
            command=self.show_more,
            width=10
        )
        more_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear,
            width=10
        )
        clear_button.pack(side=tk.LEFT, padx=5)
    
    def _read_board(self) -> Optional[List[List[int]]]:
        """Read the current board state from the GUI.
        
        Returns:
            A 9x9 board representation, or None if invalid input.
        """
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.sudoku_entries[i][j].get()
                if value == "":
                    row.append(0)
                else:
                    try:
                        num = int(value)
                        if 0 <= num <= 9:
                            row.append(num)
                        else:
                            messagebox.showerror("Error", "Invalid value detected!")
                            return None
                    except ValueError:
                        messagebox.showerror("Error", "Invalid character detected!")
                        return None
            board.append(row)
        return board
    
    def solve(self) -> None:
        """Solve the Sudoku puzzle entered in the GUI."""
        board = self._read_board()
        if board is None:
            return
        
        # Find all solutions
        self.solutions = find_all_solutions(board, max_solutions=10)
        
        if not self.solutions:
            messagebox.showerror("Error", "No solution!")
            return
        
        # Display the first solution
        self._display_solution(self.solutions[0])
        
        if len(self.solutions) == 1:
            messagebox.showinfo("Info", "Unique solution found!")
        else:
            messagebox.showinfo(
                "Info",
                f"Found {len(self.solutions)} solution(s). Click 'More' to see others."
            )
    
    def _display_solution(self, solution: List[List[int]]) -> None:
        """Display a solution in the GUI.
        
        Args:
            solution: A 9x9 solved Sudoku board.
        """
        for i in range(9):
            for j in range(9):
                if self.sudoku_entries[i][j].get() == "":
                    self.sudoku_entries[i][j].insert(0, str(solution[i][j]))
                    self.sudoku_entries[i][j].config(fg="red")
    
    def show_more(self) -> None:
        """Show additional solutions in a new window."""
        if not self.solutions:
            messagebox.showerror("Error", "No solutions available!")
            return
        
        # Create new window
        more_window = tk.Toplevel(self.root)
        more_window.title("More Solutions")
        more_window.config(bg="#F5F5DC")
        
        if len(self.solutions) == 1:
            tk.Label(
                more_window,
                text="No more solutions!",
                bg="#F5F5DC",
                font=("Arial", 12)
            ).pack(pady=20)
            return
        
        # Create scrollable frame
        canvas = tk.Canvas(more_window, bg="#F5F5DC", highlightthickness=0)
        scrollbar = tk.Scrollbar(more_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F5F5DC")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Display additional solutions
        for idx, solution in enumerate(self.solutions[1:], start=2):
            solution_label = tk.Label(
                scrollable_frame,
                text=f"Solution {idx}:",
                bg="#F5F5DC",
                font=("Arial", 12, "bold")
            )
            solution_label.pack(pady=(10, 5))
            
            solution_frame = tk.Frame(scrollable_frame, bg="#F5F5DC")
            solution_frame.pack(pady=5)
            
            for i in range(9):
                for j in range(9):
                    entry = tk.Entry(
                        solution_frame,
                        width=2,
                        font=("Arial", 16),
                        justify="center",
                        fg="blue",
                        state="readonly",
                        bg="#F5F5DC"
                    )
                    entry.grid(row=i, column=j, padx=1, pady=1)
                    entry.insert(0, str(solution[i][j]))
    
    def clear(self) -> None:
        """Clear all entries in the Sudoku grid."""
        for i in range(9):
            for j in range(9):
                self.sudoku_entries[i][j].delete(0, tk.END)
                self.sudoku_entries[i][j].config(fg="black")
        self.solutions = []


def main():
    """Main entry point for the Sudoku Solver application."""
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
