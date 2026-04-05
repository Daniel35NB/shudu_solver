#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sudoku Solver - Main Entry Point

This is the main script to run the Sudoku Solver application.
"""

import sys
import os

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sudoku_solver.gui import main

if __name__ == "__main__":
    main()
