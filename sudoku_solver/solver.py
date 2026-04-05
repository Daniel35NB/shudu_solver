# -*- coding: utf-8 -*-
"""
Sudoku Solver Module

This module contains the core logic for solving Sudoku puzzles.
"""

from typing import List, Tuple, Optional


def find_empty(board: List[List[int]]) -> Optional[Tuple[int, int]]:
    """Find the next empty cell in the Sudoku board.
    
    Args:
        board: 9x9 Sudoku board where 0 represents an empty cell.
        
    Returns:
        A tuple (row, col) of the empty cell position, or None if no empty cells.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def is_valid(board: List[List[int]], num: int, pos: Tuple[int, int]) -> bool:
    """Check if placing a number at the given position is valid.
    
    Args:
        board: 9x9 Sudoku board.
        num: Number to check (1-9).
        pos: Position (row, col) to check.
        
    Returns:
        True if the placement is valid, False otherwise.
    """
    row, col = pos
    
    # Check row
    for i in range(9):
        if board[row][i] == num and i != col:
            return False
    
    # Check column
    for i in range(9):
        if board[i][col] == num and i != row:
            return False
    
    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3
    
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    
    return True


def solve_sudoku(board: List[List[int]]) -> bool:
    """Solve a Sudoku puzzle using backtracking.
    
    Args:
        board: 9x9 Sudoku board where 0 represents empty cells.
               The board is modified in-place.
               
    Returns:
        True if a solution is found, False otherwise.
    """
    empty = find_empty(board)
    if not empty:
        return True  # No empty cells, puzzle is solved
    
    row, col = empty
    
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            
            if solve_sudoku(board):
                return True
            
            # Backtrack
            board[row][col] = 0
    
    return False


def find_all_solutions(board: List[List[int]], max_solutions: int = 10) -> List[List[List[int]]]:
    """Find all solutions for a Sudoku puzzle.
    
    Args:
        board: 9x9 Sudoku board where 0 represents empty cells.
        max_solutions: Maximum number of solutions to find.
        
    Returns:
        A list of all found solutions (each solution is a 9x9 board).
    """
    solutions = []
    
    def backtrack(current_board: List[List[int]]) -> None:
        if len(solutions) >= max_solutions:
            return
        
        empty = find_empty(current_board)
        if not empty:
            solutions.append([row[:] for row in current_board])
            return
        
        row, col = empty
        
        for num in range(1, 10):
            if is_valid(current_board, num, (row, col)):
                current_board[row][col] = num
                backtrack(current_board)
                current_board[row][col] = 0
    
    backtrack(board)
    return solutions
