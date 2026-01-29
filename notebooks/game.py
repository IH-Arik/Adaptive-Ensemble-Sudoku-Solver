import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import random
import queue
import copy
from enum import Enum
import threading

class Algorithm(Enum):
    BACKTRACKING = "Backtracking"
    DFS = "Depth-First Search"
    BFS = "Breadth-First Search"
    HEURISTIC = "Heuristic Search"
    MRV = "Minimum Remaining Values"
    FORWARD_CHECKING = "Forward Checking"
    ARC_CONSISTENCY = "Arc Consistency"

class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    VERY_HARD = "Very Hard"

class SudokuSolver:
    def __init__(self):
        self.steps = 0
        self.evaluations = 0
        self.domains = {}  # For arc consistency
    
    def is_valid(self, board, row, col, num, evaluation_callback=None):
        if evaluation_callback:
            evaluation_callback(row, col)
        
        self.evaluations += 1
        
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def find_empty(self, board, evaluation_callback=None):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if evaluation_callback:
                        evaluation_callback(i, j)
                    return (i, j)
        return None
    
    def solve_backtracking(self, board, update_ui=None, evaluation_callback=None):
        self.steps = 0
        self.evaluations = 0
        return self._backtrack(board, update_ui, evaluation_callback)
    
    def _backtrack(self, board, update_ui=None, evaluation_callback=None):
        self.steps += 1
        empty = self.find_empty(board, evaluation_callback)
        if not empty:
            return True
        
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid(board, row, col, num, evaluation_callback):
                board[row][col] = num
                
                # Update UI if callback provided
                if update_ui:
                    if not update_ui(row, col, num):
                        return False
                
                if self._backtrack(board, update_ui, evaluation_callback):
                    return True
                
                board[row][col] = 0
                if update_ui:
                    if not update_ui(row, col, 0):
                        return False
        
        return False
    
    def solve_dfs(self, board, update_ui=None, evaluation_callback=None):
        self.steps = 0
        self.evaluations = 0
        stack = []
        empty = self.find_empty(board, evaluation_callback)
        if not empty:
            return True
        
        # (board, row, col, num)
        stack.append((copy.deepcopy(board), empty[0], empty[1], 1))
        
        while stack:
            self.steps += 1
            current_board, row, col, num = stack.pop()
            
            # Skip invalid numbers
            while num <= 9 and not self.is_valid(current_board, row, col, num, evaluation_callback):
                num += 1
            
            if num > 9:
                continue
            
            # Place the number
            current_board[row][col] = num
            
            # Update UI
            if update_ui:
                if not update_ui(row, col, num):
                    return False
            
            # Find next empty cell
            next_empty = self.find_empty(current_board, evaluation_callback)
            
            # If no empty cells, puzzle is solved
            if not next_empty:
                for i in range(9):
                    for j in range(9):
                        board[i][j] = current_board[i][j]
                return True
            
            # Push the next state with num+1 (backtracking option)
            stack.append((copy.deepcopy(current_board), row, col, num + 1))
            
            # Push the next empty cell with num=1
            stack.append((copy.deepcopy(current_board), next_empty[0], next_empty[1], 1))
        
        return False
    
    def solve_bfs(self, board, update_ui=None, evaluation_callback=None):
        self.steps = 0
        self.evaluations = 0
        q = queue.Queue()
        empty = self.find_empty(board, evaluation_callback)
        if not empty:
            return True
        
        # (board, empty_cells)
        initial_board = copy.deepcopy(board)
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    empty_cells.append((i, j))
        
        q.put((initial_board, 0))  # Start with first empty cell
        
        while not q.empty():
            self.steps += 1
            current_board, cell_idx = q.get()
            
            if cell_idx >= len(empty_cells):
                # All cells filled
                for i in range(9):
                    for j in range(9):
                        board[i][j] = current_board[i][j]
                return True
            
            row, col = empty_cells[cell_idx]
            
            if evaluation_callback:
                evaluation_callback(row, col)
            
            for num in range(1, 10):
                if self.is_valid(current_board, row, col, num, evaluation_callback):
                    new_board = copy.deepcopy(current_board)
                    new_board[row][col] = num
                    
                    # Update UI
                    if update_ui:
                        if not update_ui(row, col, num):
                            return False
                    
                    q.put((new_board, cell_idx + 1))
            
            # BFS can be very slow for Sudoku, so we'll limit steps
            if self.steps > 10000:
                return False
        
        return False
    
    def solve_heuristic(self, board, update_ui=None, evaluation_callback=None):
        self.steps = 0
        self.evaluations = 0
        return self._heuristic_search(board, update_ui, evaluation_callback)
    
    def _heuristic_search(self, board, update_ui=None, evaluation_callback=None):
        empty = self.find_empty(board, evaluation_callback)
        if not empty:
            return True
        
        row, col = empty
        
        # Heuristic: Try numbers that appear less frequently first
        counts = [0] * 10
        for i in range(9):
            for j in range(9):
                if board[i][j] > 0:
                    counts[board[i][j]] += 1
        
        # Sort numbers by frequency (ascending)
        numbers = sorted(range(1, 10), key=lambda x: counts[x])
        
        for num in numbers:
            self.steps += 1
            if self.is_valid(board, row, col, num, evaluation_callback):
                board[row][col] = num
                
                # Update UI
                if update_ui:
                    if not update_ui(row, col, num):
                        return False
                
                if self._heuristic_search(board, update_ui, evaluation_callback):
                    return True
                
                board[row][col] = 0
                if update_ui:
                    if not update_ui(row, col, 0):
                        return False
        
        return False
    
    def solve_mrv(self, board, update_ui=None, evaluation_callback=None):
        self.steps = 0
        self.evaluations = 0
        return self._mrv_search(board, update_ui, evaluation_callback)
    
    def _get_legal_values(self, board, row, col, evaluation_callback=None):
        legal = []
        for num in range(1, 10):
            if self.is_valid(board, row, col, num, evaluation_callback):
                legal.append(num)
        return legal
    
    def _find_mrv(self, board, evaluation_callback=None):
        min_remaining = 10
        min_pos = None
        
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if evaluation_callback:
                        evaluation_callback(i, j)
                    
                    legal_values = self._get_legal_values(board, i, j, evaluation_callback)
                    if len(legal_values) < min_remaining:
                        min_remaining = len(legal_values)
                        min_pos = (i, j, legal_values)
                    
                    # If we find a cell with no legal values, fail fast
                    if min_remaining == 0:
                        return min_pos
        
        return min_pos
    
    def _mrv_search(self, board, update_ui=None, evaluation_callback=None):
        self.steps += 1
        
        # Find cell with minimum remaining values
        mrv = self._find_mrv(board, evaluation_callback)
        if not mrv:
            return True  # No empty cells
        
        row, col, legal_values = mrv
        
        # If no legal values for a cell, this branch fails
        if not legal_values:
            return False
        
        for num in legal_values:
            board[row][col] = num
            
            # Update UI
            if update_ui:
                if not update_ui(row, col, num):
                    return False
            
            if self._mrv_search(board, update_ui, evaluation_callback):
                return True
            
            board[row][col] = 0
            if update_ui:
                if not update_ui(row, col, 0):
                    return False
        
        return False
    
    def solve_forward_checking(self, board, update_ui=None, evaluation_callback=None):
        self.steps = 0
        self.evaluations = 0
        # Initialize domains for all cells
        domains = {}
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    domains[(i, j)] = list(range(1, 10))
                else:
                    domains[(i, j)] = [board[i][j]]
        
        # Apply initial constraints
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self._update_domains(board, domains, i, j, board[i][j])
        
        return self._forward_checking(board, domains, update_ui, evaluation_callback)
    
    def _update_domains(self, board, domains, row, col, value):
        # Remove value from domains of cells in same row, column, and box
        for i in range(9):
            # Same row
            if board[row][i] == 0 and (row, i) in domains and value in domains[(row, i)]:
                domains[(row, i)].remove(value)
            
            # Same column
            if board[i][col] == 0 and (i, col) in domains and value in domains[(i, col)]:
                domains[(i, col)].remove(value)
        
        # Same box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                r, c = start_row + i, start_col + j
                if board[r][c] == 0 and (r, c) in domains and value in domains[(r, c)]:
                    domains[(r, c)].remove(value)
    
    def _forward_checking(self, board, domains, update_ui=None, evaluation_callback=None):
        self.steps += 1
        
        # Find unassigned cell with minimum remaining values
        min_len = 10
        min_cell = None
        
        for cell, values in domains.items():
            if board[cell[0]][cell[1]] == 0 and len(values) > 0 and len(values) < min_len:
                if evaluation_callback:
                    evaluation_callback(cell[0], cell[1])
                
                min_len = len(values)
                min_cell = cell
        
        # If no unassigned cells, we're done
        if min_cell is None:
            return True
        
        row, col = min_cell
        
        # If any domain is empty, this branch fails
        for cell, values in domains.items():
            if board[cell[0]][cell[1]] == 0 and len(values) == 0:
                return False
        
        # Try each value in the domain
        for value in list(domains[(row, col)]):
            board[row][col] = value
            
            # Update UI
            if update_ui:
                if not update_ui(row, col, value):
                    return False
            
            # Save domains for backtracking
            old_domains = copy.deepcopy(domains)
            
            # Update domains
            self._update_domains(board, domains, row, col, value)
            
            # Recursively solve
            if self._forward_checking(board, domains, update_ui, evaluation_callback):
                return True
            
            # Backtrack
            board[row][col] = 0
            domains = old_domains
            
            if update_ui:
                if not update_ui(row, col, 0):
                    return False
        
        return False

    def get_domain(self, board, row, col):
        """Get the domain of possible values for a cell."""
        if board[row][col] != 0:
            return {board[row][col]}
        
        domain = set(range(1, 10))
        
        # Check row
        for j in range(9):
            if board[row][j] != 0:
                domain.discard(board[row][j])
        
        # Check column
        for i in range(9):
            if board[i][col] != 0:
                domain.discard(board[i][col])
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] != 0:
                    domain.discard(board[start_row + i][start_col + j])
        
        return domain

    def get_arcs(self):
        """Get all arcs (constraints between cells) in the Sudoku grid."""
        arcs = []
        # Generate arcs for rows, columns, and boxes
        for i in range(9):
            for j in range(9):
                # Row arcs
                for k in range(9):
                    if k != j:
                        arcs.append(((i, j), (i, k)))
                # Column arcs
                for k in range(9):
                    if k != i:
                        arcs.append(((i, j), (k, j)))
                # Box arcs
                box_row, box_col = 3 * (i // 3), 3 * (j // 3)
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        if (r, c) != (i, j):
                            arcs.append(((i, j), (r, c)))
        return arcs

    def revise(self, board, xi, xj):
        """Revise the domain of xi with respect to xj."""
        revised = False
        i, j = xi
        if board[i][j] != 0:  # Skip if cell already has a value
            return False
        
        if (i, j) not in self.domains:
            self.domains[(i, j)] = self.get_domain(board, i, j)
        
        domain_i = self.domains[(i, j)]
        domain_j = self.get_domain(board, xj[0], xj[1])
        
        for x in list(domain_i):
            # If xi=x conflicts with all possible values in xj's domain
            if len(domain_j) == 1 and x in domain_j:
                domain_i.discard(x)
                revised = True
        
        self.domains[(i, j)] = domain_i
        return revised

    def ac3(self, board, update_ui=None, evaluation_callback=None):
        """Implement AC-3 algorithm for arc consistency."""
        self.steps = 0
        self.evaluations = 0
        self.domains.clear()
        
        # Initialize queue with all arcs
        queue = self.get_arcs()
        
        while queue:
            self.steps += 1
            (xi, xj) = queue.pop(0)
            
            if evaluation_callback:
                evaluation_callback(xi[0], xi[1])
            
            if self.revise(board, xi, xj):
                if not self.domains[xi]:  # Domain is empty
                    return False
                
                # Add neighbors of xi back to queue
                neighbors = [(xi[0], k) for k in range(9) if k != xi[1]]  # Row neighbors
                neighbors += [(k, xi[1]) for k in range(9) if k != xi[0]]  # Column neighbors
                box_row, box_col = 3 * (xi[0] // 3), 3 * (xi[1] // 3)
                neighbors += [(r, c) for r in range(box_row, box_row + 3)
                            for c in range(box_col, box_col + 3)
                            if (r, c) != xi]  # Box neighbors
                
                for xk in neighbors:
                    if xk != xj:
                        queue.append((xk, xi))
        
        # After AC-3, try to fill in determined values
        filled = False
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0 and (i, j) in self.domains:
                    if len(self.domains[(i, j)]) == 1:
                        board[i][j] = list(self.domains[(i, j)])[0]
                        if update_ui:
                            if not update_ui(i, j, board[i][j]):
                                return False
                        filled = True
        
        # If we filled some values, run AC-3 again
        if filled:
            return self.ac3(board, update_ui, evaluation_callback)
        
        return True

    def solve_arc_consistency(self, board, update_ui=None, evaluation_callback=None):
        """Solve using Arc Consistency combined with backtracking."""
        self.steps = 0
        self.evaluations = 0
        
        # First, apply AC-3
        if not self.ac3(board, update_ui, evaluation_callback):
            return False
        
        # If puzzle not solved, use backtracking with the reduced domains
        if any(board[i][j] == 0 for i in range(9) for j in range(9)):
            return self._backtrack_with_ac3(board, update_ui, evaluation_callback)
        
        return True

    def _backtrack_with_ac3(self, board, update_ui=None, evaluation_callback=None):
        """Backtracking with AC-3 preprocessed domains."""
        self.steps += 1
        empty = self.find_empty(board, evaluation_callback)
        if not empty:
            return True
        
        row, col = empty
        domain = self.domains.get((row, col), self.get_domain(board, row, col))
        
        for num in domain:
            if self.is_valid(board, row, col, num, evaluation_callback):
                board[row][col] = num
                
                if update_ui:
                    if not update_ui(row, col, num):
                        return False
                
                # Apply AC-3 after each assignment
                old_domains = self.domains.copy()
                if self.ac3(board, update_ui, evaluation_callback):
                    if self._backtrack_with_ac3(board, update_ui, evaluation_callback):
                        return True
                
                # Restore domains if this branch fails
                self.domains = old_domains
                board[row][col] = 0
                if update_ui:
                    if not update_ui(row, col, 0):
                        return False
        
        return False

class SudokuGenerator:
    def __init__(self):
        self.solver = SudokuSolver()
    
    def generate_puzzle(self, difficulty):
        # Generate a solved board
        board = self._generate_solved_board()
        
        # Remove numbers based on difficulty
        if difficulty == Difficulty.EASY:
            cells_to_remove = random.randint(40, 45)
        elif difficulty == Difficulty.MEDIUM:
            cells_to_remove = random.randint(46, 52)
        elif difficulty == Difficulty.HARD:
            cells_to_remove = random.randint(53, 59)
        else:  # very hard
            cells_to_remove = random.randint(60, 64)
        
        self._remove_numbers(board, cells_to_remove)
        return board
    
    def _generate_solved_board(self):
        # Start with an empty board
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill the diagonal boxes first (these don't affect each other)
        for i in range(0, 9, 3):
            self._fill_box(board, i, i)
        
        # Solve the rest of the board
        self.solver.solve_backtracking(board)
        return board
    
    def _fill_box(self, board, row, col):
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for i in range(3):
            for j in range(3):
                board[row + i][col + j] = nums.pop()
    
    def _remove_numbers(self, board, count):
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i, j in cells[:count]:
            temp = board[i][j]
            board[i][j] = 0
            
            # Make a copy for solving
            board_copy = copy.deepcopy(board)
            
            # Count solutions
            if not self._has_unique_solution(board_copy):
                board[i][j] = temp  # Restore if removing creates multiple solutions
        
        return board
    
    def _has_unique_solution(self, board):
        # Check if the board has a unique solution
        # This is a simplified version - a full implementation would count all solutions
        return self.solver.solve_backtracking(board)

class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        self.hover_bg = kwargs.pop('hover_background', '#e0e0e0') if 'hover_background' in kwargs else '#e0e0e0'
        self.hover_fg = kwargs.pop('hover_foreground', 'black') if 'hover_foreground' in kwargs else 'black'
        self.active_bg = kwargs.pop('active_background', '#c0c0c0') if 'active_background' in kwargs else '#c0c0c0'
        
        kwargs['relief'] = kwargs.get('relief', 'flat')
        kwargs['bg'] = kwargs.get('bg', '#f0f0f0')
        kwargs['fg'] = kwargs.get('fg', 'black')
        kwargs['font'] = kwargs.get('font', ('Helvetica', 10))
        kwargs['padx'] = kwargs.get('padx', 10)
        kwargs['pady'] = kwargs.get('pady', 5)
        kwargs['borderwidth'] = kwargs.get('borderwidth', 1)
        
        super().__init__(master, **kwargs)
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
    
    def _on_enter(self, e):
        self['background'] = self.hover_bg
        self['foreground'] = self.hover_fg
    
    def _on_leave(self, e):
        self['background'] = self['bg']
        self['foreground'] = self['fg']
    
    def _on_press(self, e):
        self['background'] = self.active_bg
    
    def _on_release(self, e):
        self['background'] = self.hover_bg

class AlgorithmButton(ModernButton):
    def __init__(self, master=None, algorithm=None, command=None, **kwargs):
        self.algorithm = algorithm
        kwargs['text'] = algorithm.value if algorithm else "Algorithm"
        kwargs['command'] = command
        kwargs['width'] = kwargs.get('width', 20)
        
        # Custom styling for algorithm buttons
        kwargs['bg'] = '#e6f7ff'
        kwargs['hover_background'] = '#bae7ff'
        kwargs['active_background'] = '#91d5ff'
        
        super().__init__(master, **kwargs)

class DifficultyButton(ModernButton):
    def __init__(self, master=None, difficulty=None, command=None, **kwargs):
        self.difficulty = difficulty
        kwargs['text'] = difficulty.value if difficulty else "Difficulty"
        kwargs['command'] = command
        kwargs['width'] = kwargs.get('width', 15)
        
        # Custom styling for difficulty buttons
        if difficulty == Difficulty.EASY:
            kwargs['bg'] = '#d9f7be'
            kwargs['hover_background'] = '#b7eb8f'
            kwargs['active_background'] = '#95de64'
        elif difficulty == Difficulty.MEDIUM:
            kwargs['bg'] = '#fff1b8'
            kwargs['hover_background'] = '#ffd666'
            kwargs['active_background'] = '#ffc53d'
        elif difficulty == Difficulty.HARD:
            kwargs['bg'] = '#ffccc7'
            kwargs['hover_background'] = '#ffa39e'
            kwargs['active_background'] = '#ff7875'
        else:  # VERY_HARD
            kwargs['bg'] = '#ffadd2'
            kwargs['hover_background'] = '#ff85c0'
            kwargs['active_background'] = '#f759ab'
        
        super().__init__(master, **kwargs)

class ControlButton(ModernButton):
    def __init__(self, master=None, **kwargs):
        # Custom styling for control buttons
        kwargs['bg'] = '#f0f0f0'
        kwargs['hover_background'] = '#d9d9d9'
        kwargs['active_background'] = '#bfbfbf'
        kwargs['width'] = kwargs.get('width', 12)
        
        super().__init__(master, **kwargs)

class SudokuCell(tk.Frame):
    def __init__(self, parent, row, col, size=50, **kwargs):
        super().__init__(parent, width=size, height=size, **kwargs)
        self.parent = parent
        self.row = row
        self.col = col
        self.size = size
        self.value = tk.StringVar()
        self.original = False
        self.highlighted = False
        self.evaluation_highlight = False
        
        self.entry = tk.Entry(
            self, font=("Helvetica", 16, "bold"), width=2, justify="center",
            textvariable=self.value, bd=0
        )
        self.entry.place(relx=0.5, rely=0.5, anchor="center")
        
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.entry.bind("<KeyRelease>", self.validate_input)
        
        self.pack_propagate(False)
    
    def set_value(self, value, original=False):
        self.value.set(str(value) if value != 0 else "")
        self.original = original
        if original:
            self.entry.config(state="readonly", readonlybackground="#e0e0e0", fg="#000080")
        else:
            self.entry.config(state="normal", background="white", fg="black")
    
    def get_value(self):
        val = self.value.get()
        return int(val) if val.isdigit() else 0
    
    def highlight(self, color="#ffeb99"):
        self.highlighted = True
        self.config(background=color)
    
    def highlight_evaluation(self, color="#e6f7ff"):
        self.evaluation_highlight = True
        self.config(background=color)
        self.after(200, self.remove_evaluation_highlight)
    
    def remove_evaluation_highlight(self):
        if self.evaluation_highlight and not self.highlighted:
            self.evaluation_highlight = False
            self.config(background="white")
    
    def unhighlight(self):
        self.highlighted = False
        self.evaluation_highlight = False
        self.config(background="white")
    
    def on_focus_in(self, event):
        if not self.original:
            self.entry.config(background="#f0f0ff")
    
    def on_focus_out(self, event):
        if not self.original and not self.highlighted and not self.evaluation_highlight:
            self.entry.config(background="white")
    
    def validate_input(self, event):
        val = self.value.get()
        if val and (not val.isdigit() or int(val) < 1 or int(val) > 9):
            self.value.set("")
        elif len(val) > 1:
            self.value.set(val[-1])
        
        # Notify the parent grid of the change
        if hasattr(self.parent, "on_cell_change"):
            self.parent.on_cell_change()

class SudokuGrid(tk.Frame):
    def __init__(self, parent, cell_size=50, **kwargs):
        super().__init__(parent, **kwargs)
        self.cell_size = cell_size
        self.cells = []
        self.solver = SudokuSolver()
        self.solving = False
        self.paused = False
        self.solve_thread = None
        self.step_delay = 0.05  # Default delay between steps
        
        # Create the grid
        self.create_grid()
    
    def create_grid(self):
        # Create a frame for each 3x3 box with a distinct border
        for box_row in range(3):
            for box_col in range(3):
                box_frame = tk.Frame(
                    self,
                    borderwidth=2,
                    relief="solid"
                )
                box_frame.grid(row=box_row, column=box_col, padx=1, pady=1)
                
                # Create cells within each box
                for i in range(3):
                    if len(self.cells) <= box_row * 3 + i:
                        self.cells.append([])
                    for j in range(3):
                        cell_frame = tk.Frame(
                            box_frame,
                            width=self.cell_size,
                            height=self.cell_size,
                            borderwidth=1,
                            relief="solid",
                            background="white"
                        )
                        cell_frame.grid(row=i, column=j, padx=1, pady=1)
                        cell_frame.grid_propagate(False)
                        
                        cell = SudokuCell(cell_frame, box_row * 3 + i, box_col * 3 + j, self.cell_size)
                        cell.pack(fill="both", expand=True)
                        self.cells[box_row * 3 + i].append(cell)
    
    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(self.cells[i][j].get_value())
            board.append(row)
        return board
    
    def set_board(self, board, original=False):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set_value(board[i][j], original and board[i][j] != 0)
                self.cells[i][j].unhighlight()
    
    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set_value(0, False)
                self.cells[i][j].unhighlight()
    
    def highlight_cell(self, row, col, color="#ffeb99"):
        self.cells[row][col].highlight(color)
        self.update()
    
    def highlight_evaluation(self, row, col):
        self.cells[row][col].highlight_evaluation()
        self.update()
    
    def unhighlight_all(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].unhighlight()
        self.update()
    
    def on_cell_change(self):
        # This method is called when a cell value changes
        # Could be used for validation or UI updates
        pass
    
    def solve(self, algorithm, visualize=True, step_delay=0.05):
        if self.solving:
            return
        
        self.step_delay = step_delay
        self.solving = True
        self.paused = False
        
        # Start solving in a separate thread to keep UI responsive
        self.solve_thread = threading.Thread(
            target=self._solve_thread, 
            args=(algorithm, visualize)
        )
        self.solve_thread.daemon = True
        self.solve_thread.start()
    
    def _solve_thread(self, algorithm, visualize):
        board = self.get_board()
        
        # Create callbacks for visualization
        def update_ui(row, col, value):
            if not visualize or not self.solving or self.paused:
                return False  # Signal to stop solving
            
            self.cells[row][col].set_value(value, False)
            self.highlight_cell(row, col)
            time.sleep(self.step_delay)
            return True  # Continue solving
        
        def evaluation_callback(row, col):
            if not visualize or not self.solving or self.paused:
                return False
            
            self.highlight_evaluation(row, col)
            time.sleep(self.step_delay * 0.5)  # Shorter delay for evaluation
            return True
        
        # Solve using the selected algorithm
        solved = False
        if algorithm == Algorithm.BACKTRACKING:
            solved = self.solver.solve_backtracking(board, update_ui, evaluation_callback)
        elif algorithm == Algorithm.DFS:
            solved = self.solver.solve_dfs(board, update_ui, evaluation_callback)
        elif algorithm == Algorithm.BFS:
            solved = self.solver.solve_bfs(board, update_ui, evaluation_callback)
        elif algorithm == Algorithm.HEURISTIC:
            solved = self.solver.solve_heuristic(board, update_ui, evaluation_callback)
        elif algorithm == Algorithm.MRV:
            solved = self.solver.solve_mrv(board, update_ui, evaluation_callback)
        elif algorithm == Algorithm.FORWARD_CHECKING:
            solved = self.solver.solve_forward_checking(board, update_ui, evaluation_callback)
        elif algorithm == Algorithm.ARC_CONSISTENCY:
            solved = self.solver.solve_arc_consistency(board, update_ui, evaluation_callback)
        
        # Update UI with the result
        if solved and self.solving and not self.paused:
            self.set_board(board)
            messagebox.showinfo("Success", f"Puzzle solved using {algorithm.value}!")
        elif not self.paused:
            messagebox.showinfo("Failed", f"Could not solve the puzzle using {algorithm.value}.")
        
        self.solving = False
        self.unhighlight_all()
    
    def pause_solving(self):
        self.paused = True
    
    def resume_solving(self):
        if self.paused and self.solving:
            self.paused = False
            self.solve(self.current_algorithm, True, self.step_delay)
    
    def stop_solving(self):
        self.solving = False
        self.paused = False
        if self.solve_thread and self.solve_thread.is_alive():
            self.solve_thread.join(0.1)
        self.unhighlight_all()

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("1000x750")
        self.root.minsize(900, 700)
        self.root.configure(bg="#f5f5f5")
        
        # Set up styles
        self.setup_styles()
        
        # Create widgets
        self.create_widgets()
        
        # Initialize game components
        self.generator = SudokuGenerator()
        self.current_algorithm = Algorithm.BACKTRACKING
        self.step_delay = 0.05
        
        # Set up responsive layout
        self.setup_responsive_layout()
    
    def setup_styles(self):
        # Configure ttk styles
        style = ttk.Style()
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5", font=("Helvetica", 11))
        style.configure("TLabelframe", background="#f5f5f5")
        style.configure("TLabelframe.Label", background="#f5f5f5", font=("Helvetica", 11, "bold"))
        style.configure("Header.TLabel", font=("Helvetica", 20, "bold"))
        style.configure("Stats.TLabel", font=("Helvetica", 10))
        
        # Configure scale style
        style.configure("Horizontal.TScale", background="#f5f5f5")
    
    def create_widgets(self):
        # Main container
        self.main_container = ttk.Frame(self.root, padding=10)
        self.main_container.pack(fill="both", expand=True)
        
        # Header
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Sudoku Solver", style="Header.TLabel")
        title_label.pack(side="left", padx=10)
        
        # Main content area - using grid for better responsiveness
        content_frame = ttk.Frame(self.main_container)
        content_frame.pack(fill="both", expand=True)
        content_frame.columnconfigure(0, weight=3)  # Grid area
        content_frame.columnconfigure(1, weight=2)  # Controls area
        
        # Left side - Sudoku grid
        grid_frame = ttk.Frame(content_frame, padding=10)
        grid_frame.grid(row=0, column=0, sticky="nsew")
        
        # Create a frame to center the grid
        center_frame = ttk.Frame(grid_frame)
        center_frame.pack(expand=True)
        
        # Create the Sudoku grid with a fixed cell size
        cell_size = 55  # Larger cells for better visibility
        self.sudoku_grid = SudokuGrid(center_frame, cell_size=cell_size)
        self.sudoku_grid.pack(padx=10, pady=10)
        
        # Right side - Controls
        controls_frame = ttk.Frame(content_frame, padding=10)
        controls_frame.grid(row=0, column=1, sticky="nsew")
        
        # Algorithm section
        algo_frame = ttk.LabelFrame(controls_frame, text="Solving Algorithms", padding=10)
        algo_frame.pack(fill="x", pady=5)
        
        # Create algorithm buttons in a grid layout
        algo_buttons_frame = ttk.Frame(algo_frame)
        algo_buttons_frame.pack(fill="x", pady=5)
        
        row, col = 0, 0
        for algo in Algorithm:
            btn = AlgorithmButton(
                algo_buttons_frame,
                algorithm=algo,
                command=lambda a=algo: self.select_algorithm(a)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            # Update row and column for next button
            col += 1
            if col > 1:  # 2 buttons per row
                col = 0
                row += 1
        
        # Currently selected algorithm
        self.algorithm_label = ttk.Label(
            algo_frame, 
            text=f"Selected: {Algorithm.BACKTRACKING.value}",
            font=("Helvetica", 10, "bold")
        )
        self.algorithm_label.pack(pady=5)
        
        # Difficulty section
        difficulty_frame = ttk.LabelFrame(controls_frame, text="Generate Puzzle", padding=10)
        difficulty_frame.pack(fill="x", pady=5)
        
        difficulty_buttons_frame = ttk.Frame(difficulty_frame)
        difficulty_buttons_frame.pack(fill="x", pady=5)
        
        # Create difficulty buttons in a row
        for i, diff in enumerate(Difficulty):
            btn = DifficultyButton(
                difficulty_buttons_frame,
                difficulty=diff,
                command=lambda d=diff: self.generate_puzzle(d)
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            difficulty_buttons_frame.columnconfigure(i, weight=1)
        
        # Speed control
        speed_frame = ttk.LabelFrame(controls_frame, text="Visualization Speed", padding=10)
        speed_frame.pack(fill="x", pady=5)
        
        speed_control_frame = ttk.Frame(speed_frame)
        speed_control_frame.pack(fill="x", pady=5)
        
        ttk.Label(speed_control_frame, text="Fast").pack(side="left", padx=5)
        
        self.speed_var = tk.DoubleVar(value=0.05)
        speed_scale = ttk.Scale(
            speed_control_frame, 
            from_=0.001, 
            to=0.2, 
            orient="horizontal", 
            variable=self.speed_var,
            length=200
        )
        speed_scale.pack(side="left", padx=5, fill="x", expand=True)
        
        ttk.Label(speed_control_frame, text="Slow").pack(side="left", padx=5)
        
        # Control buttons
        controls_buttons_frame = ttk.LabelFrame(controls_frame, text="Controls", padding=10)
        controls_buttons_frame.pack(fill="x", pady=5)
        
        # First row of control buttons
        btn_row1 = ttk.Frame(controls_buttons_frame)
        btn_row1.pack(fill="x", pady=5)
        
        self.solve_btn = ControlButton(btn_row1, text="Solve", command=self.solve)
        self.solve_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        self.pause_btn = ControlButton(btn_row1, text="Pause", command=self.pause, state="disabled")
        self.pause_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        self.resume_btn = ControlButton(btn_row1, text="Resume", command=self.resume, state="disabled")
        self.resume_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        # Second row of control buttons
        btn_row2 = ttk.Frame(controls_buttons_frame)
        btn_row2.pack(fill="x", pady=5)
        
        self.stop_btn = ControlButton(btn_row2, text="Stop", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        self.clear_btn = ControlButton(btn_row2, text="Clear", command=self.clear)
        self.clear_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        self.show_solution_btn = ControlButton(btn_row2, text="Show Solution", command=self.show_solution)
        self.show_solution_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        # Add Compare button to the second row of control buttons
        self.compare_btn = ControlButton(btn_row2, text="Compare", command=self.compare_algorithms)
        self.compare_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        # Status and statistics
        status_frame = ttk.LabelFrame(controls_frame, text="Status & Statistics", padding=10)
        status_frame.pack(fill="x", pady=5)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, wraplength=300)
        status_label.pack(fill="x", pady=5)
        
        # Statistics
        self.stats_var = tk.StringVar(value="No algorithm run yet")
        stats_label = ttk.Label(status_frame, textvariable=self.stats_var, style="Stats.TLabel", wraplength=300)
        stats_label.pack(fill="x", pady=5)
        
        # Progress bar for solving visualization
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            status_frame, 
            orient="horizontal", 
            length=200, 
            mode="determinate",
            variable=self.progress_var
        )
        self.progress_bar.pack(fill="x", pady=5)
    
    def setup_responsive_layout(self):
        # Make the layout respond to window resizing
        self.root.bind("<Configure>", self.on_window_resize)
    
    def on_window_resize(self, event):
        # This method can be used to adjust UI elements based on window size
        pass
    
    def select_algorithm(self, algorithm):
        self.current_algorithm = algorithm
        self.algorithm_label.config(text=f"Selected: {algorithm.value}")
    
    def solve(self):
        # Get the selected algorithm
        algorithm = self.current_algorithm
        
        # Update UI state
        self.solve_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.resume_btn.config(state="disabled")
        self.clear_btn.config(state="disabled")
        self.show_solution_btn.config(state="disabled")
        
        # Update status
        self.status_var.set(f"Solving with {algorithm.value}...")
        
        # Reset progress bar
        self.progress_var.set(0)
        
        # Get speed
        self.step_delay = self.speed_var.get()
        
        # Start solving
        start_time = time.time()
        self.sudoku_grid.solve(algorithm, True, self.step_delay)
        
        # Monitor the solving process
        self.check_solving_status(start_time)
    
    def check_solving_status(self, start_time):
        if self.sudoku_grid.solving:
            # Update progress bar (approximate)
            if hasattr(self.sudoku_grid.solver, 'steps'):
                # Estimate progress (very approximate)
                progress = min(self.sudoku_grid.solver.steps / 1000, 100)
                self.progress_var.set(progress)
            
            # Still solving, check again later
            self.root.after(100, lambda: self.check_solving_status(start_time))
        else:
            # Solving finished
            end_time = time.time()
            elapsed = end_time - start_time
            
            # Update progress bar to 100%
            self.progress_var.set(100)
            
            # Update statistics
            steps = self.sudoku_grid.solver.steps
            evals = self.sudoku_grid.solver.evaluations
            self.stats_var.set(
                f"Algorithm: {self.current_algorithm.value}\n"
                f"Time: {elapsed:.2f} seconds\n"
                f"Steps: {steps}\n"
                f"Cell Evaluations: {evals}"
            )
            
            # Update UI state
            self.solve_btn.config(state="normal")
            self.pause_btn.config(state="disabled")
            self.resume_btn.config(state="disabled")
            self.stop_btn.config(state="disabled")
            self.clear_btn.config(state="normal")
            self.show_solution_btn.config(state="normal")
            
            # Update status
            if self.sudoku_grid.paused:
                self.status_var.set("Solving paused")
            else:
                self.status_var.set("Ready")
    
    def pause(self):
        if self.sudoku_grid.solving and not self.sudoku_grid.paused:
            self.sudoku_grid.pause_solving()
            self.status_var.set("Solving paused")
            self.pause_btn.config(state="disabled")
            self.resume_btn.config(state="normal")
    
    def resume(self):
        if self.sudoku_grid.solving and self.sudoku_grid.paused:
            self.sudoku_grid.resume_solving()
            self.status_var.set(f"Solving with {self.current_algorithm.value}...")
            self.pause_btn.config(state="normal")
            self.resume_btn.config(state="disabled")
    
    def stop(self):
        if self.sudoku_grid.solving:
            self.sudoku_grid.stop_solving()
            self.status_var.set("Solving stopped")
            
            # Update UI state
            self.solve_btn.config(state="normal")
            self.pause_btn.config(state="disabled")
            self.resume_btn.config(state="disabled")
            self.stop_btn.config(state="disabled")
            self.clear_btn.config(state="normal")
            self.show_solution_btn.config(state="normal")
    
    def clear(self):
        self.sudoku_grid.clear_board()
        self.status_var.set("Ready")
        self.stats_var.set("No algorithm run yet")
        self.progress_var.set(0)
    
    def generate_puzzle(self, difficulty):
        self.status_var.set(f"Generating {difficulty.value} puzzle...")
        self.root.update()
        
        # Generate the puzzle
        board = self.generator.generate_puzzle(difficulty)
        self.sudoku_grid.set_board(board, original=True)
        
        self.status_var.set(f"Generated {difficulty.value} puzzle")
    
    def show_solution(self):
        # Get the current board
        board = self.sudoku_grid.get_board()
        
        # Make a copy to solve
        board_copy = copy.deepcopy(board)
        
        # Try to solve with backtracking (fastest)
        self.status_var.set("Finding solution...")
        self.root.update()
        
        if self.sudoku_grid.solver.solve_backtracking(board_copy):
            # Show the solution but mark cells as non-original
            original_board = self.sudoku_grid.get_board()
            for i in range(9):
                for j in range(9):
                    # Only update empty cells
                    if original_board[i][j] == 0:
                        self.sudoku_grid.cells[i][j].set_value(board_copy[i][j], False)
                        # Highlight solution cells
                        self.sudoku_grid.cells[i][j].highlight("#e6fffb")
            
            self.status_var.set("Solution displayed (highlighted in blue)")
        else:
            messagebox.showinfo("No Solution", "This puzzle has no solution.")
            self.status_var.set("Ready")
    
    def compare_algorithms(self):
        # Get current board state
        board = self.sudoku_grid.get_board()
        
        # Check if board is empty
        if all(board[i][j] == 0 for i in range(9) for j in range(9)):
            messagebox.showwarning("Empty Board", "Please enter a puzzle or generate one before comparing algorithms.")
            return
        
        # Create comparison window
        ComparisonWindow(self.root, board)

class ComparisonWindow(tk.Toplevel):
    def __init__(self, parent, board):
        super().__init__(parent)
        self.title("Algorithm Comparison")
        self.geometry("800x600")
        self.board = [row[:] for row in board]  # Make a deep copy
        
        # Configure the window
        self.configure(bg="#f5f5f5")
        self.resizable(True, True)
        
        # Create main container
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Create scrollable frame for results
        canvas = tk.Canvas(main_frame, bg="#f5f5f5")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.results_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas for results frame
        canvas_frame = canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        
        # Configure canvas scrolling
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.results_frame.bind("<Configure>", configure_scroll)
        
        # Make canvas resize with window
        def resize_canvas(event):
            canvas.itemconfig(canvas_frame, width=event.width)
        canvas.bind("<Configure>", resize_canvas)
        
        # Create header
        header_frame = ttk.Frame(self.results_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(header_frame, text="Algorithm Comparison", 
                 style="Header.TLabel").pack(pady=10)
        
        # Create table headers
        self.create_table_header()
        
        # Start comparison
        self.start_comparison()
    
    def create_table_header(self):
        header_frame = ttk.Frame(self.results_frame)
        header_frame.pack(fill="x", pady=5)
        
        headers = ["Algorithm", "Time (s)", "Steps", "Evaluations", "Success"]
        for i, header in enumerate(headers):
            frame = ttk.Frame(header_frame)
            frame.grid(row=0, column=i, padx=5, sticky="ew")
            frame.columnconfigure(0, weight=1)
            
            ttk.Label(frame, text=header, font=("Helvetica", 10, "bold")).pack(pady=5)
        
        header_frame.grid_columnconfigure(0, weight=2)  # Algorithm name column
        for i in range(1, 5):
            header_frame.grid_columnconfigure(i, weight=1)
        
        ttk.Separator(self.results_frame, orient="horizontal").pack(fill="x", pady=5)
    
    def add_result_row(self, algorithm, time, steps, evaluations, success):
        row_frame = ttk.Frame(self.results_frame)
        row_frame.pack(fill="x", pady=2)
        
        # Algorithm name with colored background based on performance
        algo_frame = ttk.Frame(row_frame)
        algo_frame.grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Label(algo_frame, text=algorithm.value).pack(pady=5)
        
        # Results
        ttk.Label(row_frame, text=f"{time:.3f}").grid(row=0, column=1, padx=5)
        ttk.Label(row_frame, text=str(steps)).grid(row=0, column=2, padx=5)
        ttk.Label(row_frame, text=str(evaluations)).grid(row=0, column=3, padx=5)
        
        success_text = "✓" if success else "✗"
        success_color = "green" if success else "red"
        success_label = ttk.Label(row_frame, text=success_text, foreground=success_color)
        success_label.grid(row=0, column=4, padx=5)
        
        row_frame.grid_columnconfigure(0, weight=2)  # Algorithm name column
        for i in range(1, 5):
            row_frame.grid_columnconfigure(i, weight=1)
        
        ttk.Separator(self.results_frame, orient="horizontal").pack(fill="x")
    
    def start_comparison(self):
        def run_comparison():
            solver = SudokuSolver()
            results = []
            
            for algorithm in Algorithm:
                # Create a copy of the board for each algorithm
                board_copy = [row[:] for row in self.board]
                
                # Time the solving process
                start_time = time.time()
                
                # Solve with the current algorithm
                if algorithm == Algorithm.BACKTRACKING:
                    success = solver.solve_backtracking(board_copy)
                elif algorithm == Algorithm.DFS:
                    success = solver.solve_dfs(board_copy)
                elif algorithm == Algorithm.BFS:
                    success = solver.solve_bfs(board_copy)
                elif algorithm == Algorithm.HEURISTIC:
                    success = solver.solve_heuristic(board_copy)
                elif algorithm == Algorithm.MRV:
                    success = solver.solve_mrv(board_copy)
                elif algorithm == Algorithm.FORWARD_CHECKING:
                    success = solver.solve_forward_checking(board_copy)
                elif algorithm == Algorithm.ARC_CONSISTENCY:
                    success = solver.solve_arc_consistency(board_copy)
                
                end_time = time.time()
                solve_time = end_time - start_time
                
                # Add results
                results.append({
                    'algorithm': algorithm,
                    'time': solve_time,
                    'steps': solver.steps,
                    'evaluations': solver.evaluations,
                    'success': success
                })
            
            # Sort results by time
            results.sort(key=lambda x: x['time'])
            
            # Update UI with results
            for result in results:
                self.add_result_row(
                    result['algorithm'],
                    result['time'],
                    result['steps'],
                    result['evaluations'],
                    result['success']
                )
        
        # Run comparison in a separate thread
        threading.Thread(target=run_comparison, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()