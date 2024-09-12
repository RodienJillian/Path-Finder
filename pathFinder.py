import tkinter as tk
from collections import deque

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid_move(x, y, grid, visited):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0 and not visited[x][y]

def bfs_floodfill(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    parent = [[None for _ in range(cols)] for _ in range(rows)]
    
    queue = deque([start])
    visited[start[0]][start[1]] = True
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) == goal:
            return reconstruct_path(parent, start, goal)
        
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if is_valid_move(nx, ny, grid, visited):
                visited[nx][ny] = True
                parent[nx][ny] = (x, y)  
                queue.append((nx, ny))
    
    return None

def reconstruct_path(parent, start, goal):
    # Reconstruct the path from goal to start using the parent pointers.
    path = []
    x, y = goal
    while (x, y) != start:
        path.append((x, y))
        x, y = parent[x][y]
    path.append(start)
    return path[::-1] 

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinder")
        self.root.geometry("600x700") 
        self.root.resizable(False, False)
        self.root.configure(bg="gray")

        self.grid_size = (20, 20)
        self.cell_size = 27
        
        self.animation_id = None 
        
        self.grid = [[0 for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]

        self.unwalkable_path = [
            (1,1), (1,2), (1,3), (2,2), (2,3), (3,2), (3,3), (4,5), (5,5), (6,5), (1,7), (1,8), (2,7), (2,8), (3,7), (3,8), (8,6), (8,7), (8,8), (8,9),
            (5,4), (8,0), (8,1), (7,1), (7,2), (12,17), (12,18), (13,17), (13,18), (18,16), (18,17), (18,18), (18,19), (15,14), (18,10), (18,11), (17,11), (17,12), (0,14),
            (16,12), (15,12), (14,12), (13,12), (12,12), (11,12), (14,15), (11,11), (11,12), (11,13), (12,12), (12,13), (13,12), (13,13), (14,15), (3,15), (4,15), (5,15),
            (6,15), (5,16), (5,17), (4,14), (3,14), (4,14), (5,14), (18,6), (19,6), (13,6), (7,14), (8,15), (9,16), (4,12), (4,13), (5,13),
            (6,14), (13,1), (14,1), (15,1), (16,1), (14,2), (15,2), (16,2), (14,3), (15,3), (16,3), (14,7), (13,8)
        ]
      
        for x, y in self.unwalkable_path:
            self.grid[x][y] = 1
        
        self.start = (19, 19)
        self.goal = (0, 0)
        
        self.path = bfs_floodfill(self.grid, self.start, self.goal)
        
        self.canvas = tk.Canvas(root, width=540, height=540) 
        self.canvas.pack(pady=10)
        self.draw_grid(self.grid)
        
        if self.path:
            self.animate_path(0)  
        
        self.bottom_frame = tk.Frame(self.root, bg="gray")
        self.bottom_frame.pack(pady=10, fill=tk.X)

        self.left_frame = tk.Frame(self.bottom_frame, bg="gray")
        self.left_frame.pack(side=tk.LEFT, padx=20)

        self.start_entry_label = tk.Label(self.left_frame, text="Start (row, col) ex. 0,0:", font=("Candara", 12, "bold"), bg="gray")
        self.start_entry_label.grid(row=0, column=0, padx=5)
        self.start_entry = tk.Entry(self.left_frame, width=10)
        self.start_entry.grid(row=0, column=1, padx=5)

        self.goal_entry_label = tk.Label(self.left_frame, text="Goal (row, col) ex. 0,0:", font=("Candara", 12, "bold"), bg="gray")
        self.goal_entry_label.grid(row=1, column=0, padx=5)
        self.goal_entry = tk.Entry(self.left_frame, width=10)
        self.goal_entry.grid(row=1, column=1, padx=5)

        self.update_button = tk.Button(self.left_frame, text="Find Path", font=("Candara", 12, "bold"), command=self.set_start_goal, bg="lightgray")
        self.update_button.grid(row=2, columnspan=2, pady=10)

        self.right_frame = tk.Frame(self.bottom_frame, bg="gray")
        self.right_frame.pack(side=tk.RIGHT, padx=20)

        self.restart_button = tk.Button(self.right_frame, text="Restart Path Finding", font=("Candara", 12, "bold"), command=self.restart_animation, bg="lightgray")
        self.restart_button.pack(pady=10)

    def draw_grid(self, grid, char_pos=None):
        self.canvas.delete("all")
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "lightblue" 
                text = ""
                
                if (r, c) == self.start:
                    color = "green"
                    text = "֎"
                elif (r, c) == self.goal:
                    color = "red"
                    text = "×"
                elif grid[r][c] == 1:
                    color = "black"
                elif grid[r][c] == '*':
                    color = "yellow"
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                if text:
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text, font=("Arial", 20))
               
                if char_pos and char_pos == (r, c):
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="🚶", font=("Arial", 20, "bold"), fill="black")

    def animate_path(self, i):
        # Animate the pathfinding process with a moving character.
        if i < len(self.path):
            x, y = self.path[i]
            self.grid[x][y] = '*'  
            self.draw_grid(self.grid, char_pos=(x, y))
            self.animation_id = self.root.after(250, self.animate_path, i + 1)
        else:
            self.animation_id = None 

    def set_start_goal(self):
        # Set start and goal positions based on user input.
        try:
           
            start_input = self.start_entry.get().split(',')
            goal_input = self.goal_entry.get().split(',')
            start = (int(start_input[0].strip()), int(start_input[1].strip()))
            goal = (int(goal_input[0].strip()), int(goal_input[1].strip()))
        
            self.start = start
            self.goal = goal
            
            self.restart_animation()
        except (ValueError, IndexError):
            print("Invalid input! Please enter valid coordinates as 'row, col'.")

    def restart_animation(self):
        # Restart the pathfinding animation.
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        
        self.grid = [[0 for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]
        for x, y in self.unwalkable_path:
            self.grid[x][y] = 1
            
        self.path = bfs_floodfill(self.grid, self.start, self.goal)
        if self.path:
            self.animate_path(0)

root = tk.Tk()
app = PathfindingApp(root)
root.mainloop()
