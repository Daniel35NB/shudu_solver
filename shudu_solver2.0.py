# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

# 数独求解函数
def solve_sudoku(board):
    # 找到下一个空格
    empty = find_empty(board)
    if not empty:
        return True  # 如果没有空格了，表示数独已解决
    row, col = empty

    # 尝试填入数字
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num

            # 递归求解
            if solve_sudoku(board):
                return True

            # 如果填入的数字导致无解，则恢复空格
            board[row][col] = 0

    return False

# 检查填入的数字是否合法
def is_valid(board, num, pos):
    # 检查行是否合法
    for i in range(9):
        if board[pos[0]][i] == num and i != pos[1]:
            return False

    # 检查列是否合法
    for i in range(9):
        if board[i][pos[1]] == num and i != pos[0]:
            return False

    # 检查3x3宫格是否合法
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

# 找到数独中的空格
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

# 创建主界面
root = tk.Tk()
root.title("Sudoku Solver")
root.config(bg="#F5F5DC")  # 设置背景颜色

# 创建数独方格
sudoku_frame = tk.Frame(root, bg="#F5F5DC")  # 设置数独方格背景颜色
sudoku_frame.pack()

sudoku_entries = []
for i in range(9):
    row_entries = []
    for j in range(9):
        entry = tk.Entry(sudoku_frame, width=2, font=("Arial", 16), justify="center")
        entry.grid(row=i, column=j)
        entry.config(bg="#F5F5DC")  # 设置格子背景颜色
        row_entries.append(entry)
    sudoku_entries.append(row_entries)

# 创建解决按钮
def solve():
    global solutions
    # 读取输入的数独题目
    sudoku_board = []
    for i in range(9):
        row = []
        for j in range(9):
            value = sudoku_entries[i][j].get()
            if value == "":
                row.append(0)
            else:
                try:
                    num = int(value)
                    if 0 <= num <= 9:
                        row.append(num)
                    else:
                        messagebox.showerror("Error", "Invalid value detected!")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Invalid character detected!")
                    return
        sudoku_board.append(row)

    # 解决数独
    solutions = []
    if solve_sudoku(sudoku_board):
        solutions.append([row[:] for row in sudoku_board])
        # 在数独方格中显示解决结果
        for i in range(9):
            for j in range(9):
                if sudoku_entries[i][j].get() == "":
                    sudoku_entries[i][j].insert(0, sudoku_board[i][j])
                    sudoku_entries[i][j].config({"fg": "red"})
    else:
        messagebox.showerror("Error", "No solution!")

# 创建More按钮
def show_more():
    if not solutions:
        messagebox.showerror("Error", "No solutions available!")
        return
    
    # 创建新的窗口来显示更多的解决方案
    more_window = tk.Toplevel(root)
    more_window.title("More Solutions")
    more_window.config(bg="#F5F5DC")  # 设置背景颜色

    # 创建滚动条和帧来容纳解决方案
    scrollbar = tk.Scrollbar(more_window, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    solutions_frame = tk.Frame(more_window, bg="#F5F5DC")  # 设置帧背景颜色
    solutions_frame.pack()

    if len(solutions) == 1:
        # 如果只有一个解，则显示"No more solutions!"
        tk.Label(solutions_frame, text="No more solutions!", bg="#F5F5DC").pack()
    else:
        # 在帧中显示解决方案
        for solution in solutions[1:]:
            solution_frame = tk.Frame(solutions_frame, bg="#F5F5DC")  # 设置解决方案帧背景颜色
            solution_frame.pack(pady=5)

            for i in range(9):
                for j in range(9):
                    entry = tk.Entry(solution_frame, width=2, font=("Arial", 16), justify="center")
                    entry.grid(row=i, column=j)
                    entry.insert(0, solution[i][j])
                    entry.config({"fg": "blue", "state": "readonly", "bg": "#F5F5DC"})  # 设置文本颜色和只读状态

# 创建按钮
solve_button = tk.Button(root, text="Solve", command=solve)
solve_button.pack(pady=5)

more_button = tk.Button(root, text="More", command=show_more)
more_button.pack(pady=5)

root.mainloop()
