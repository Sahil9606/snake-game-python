import tkinter as tk
import random


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Classic Snake Game")
        self.root.resizable(False, False)

        # Game constants
        self.CELL_SIZE = 20
        self.GRID_WIDTH = 30
        self.GRID_HEIGHT = 30
        self.CANVAS_WIDTH = self.CELL_SIZE * self.GRID_WIDTH
        self.CANVAS_HEIGHT = self.CELL_SIZE * self.GRID_HEIGHT
        self.GAME_SPEED = 100  # milliseconds

        # Colors
        self.BG_COLOR = "#000000"
        self.SNAKE_COLOR = "#00FF00"
        self.FOOD_COLOR = "#FF0000"
        self.TEXT_COLOR = "#FFFFFF"

        # Game variables
        self.snake = [(15, 15), (14, 15), (13, 15)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = None
        self.score = 0
        self.game_running = False
        self.game_over = False

        # UI
        self.create_ui()

        # Controls
        self.root.bind("<KeyPress>", self.on_key_press)

        # Start game
        self.place_food()
        self.start_game()

    def create_ui(self):
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        main_frame.pack(padx=10, pady=10)

        self.score_label = tk.Label(
            main_frame,
            text=f"Score: {self.score}",
            font=("Arial", 16, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        )
        self.score_label.pack(pady=(0, 5))

        self.canvas = tk.Canvas(
            main_frame,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            bg=self.BG_COLOR,
            highlightthickness=2,
            highlightbackground=self.SNAKE_COLOR
        )
        self.canvas.pack()

        instructions = tk.Label(
            main_frame,
            text="Use Arrow Keys to Move | Press R to Restart",
            font=("Arial", 10),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        )
        instructions.pack(pady=(5, 0))

    def place_food(self):
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def on_key_press(self, event):
        key = event.keysym

        if key == "Up" and self.direction != "Down":
            self.next_direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.next_direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.next_direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.next_direction = "Right"
        elif key.lower() == "r":
            self.restart_game()

    def move_snake(self):
        if not self.game_running or self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        else:
            new_head = (head_x + 1, head_y)

        # Wall collision
        if (
            new_head[0] < 0 or new_head[0] >= self.GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= self.GRID_HEIGHT
        ):
            self.end_game()
            return

        # Self collision
        if new_head in self.snake:
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.update_score()
            self.place_food()
        else:
            self.snake.pop()

        self.draw_game()
        self.root.after(self.GAME_SPEED, self.move_snake)

    def draw_game(self):
        self.canvas.delete("all")

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            x1 = x * self.CELL_SIZE
            y1 = y * self.CELL_SIZE
            x2 = x1 + self.CELL_SIZE
            y2 = y1 + self.CELL_SIZE

            color = "#00FF00" if i == 0 else "#00CC00"

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline=self.BG_COLOR
            )

        # Draw food
        if self.food:
            x, y = self.food
            x1 = x * self.CELL_SIZE
            y1 = y * self.CELL_SIZE
            x2 = x1 + self.CELL_SIZE
            y2 = y1 + self.CELL_SIZE

            self.canvas.create_oval(
                x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                fill=self.FOOD_COLOR,
                outline=self.FOOD_COLOR
            )

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def start_game(self):
        self.game_running = True
        self.game_over = False
        self.draw_game()
        self.move_snake()

    def end_game(self):
        self.game_over = True
        self.game_running = False

        self.canvas.create_text(
            self.CANVAS_WIDTH // 2,
            self.CANVAS_HEIGHT // 2 - 20,
            text="GAME OVER",
            font=("Arial", 32, "bold"),
            fill=self.TEXT_COLOR
        )
        self.canvas.create_text(
            self.CANVAS_WIDTH // 2,
            self.CANVAS_HEIGHT // 2 + 20,
            text=f"Final Score: {self.score}",
            font=("Arial", 20),
            fill=self.TEXT_COLOR
        )
        self.canvas.create_text(
            self.CANVAS_WIDTH // 2,
            self.CANVAS_HEIGHT // 2 + 50,
            text="Press R to Restart",
            font=("Arial", 14),
            fill=self.SNAKE_COLOR
        )

    def restart_game(self):
        self.snake = [(15, 15), (14, 15), (13, 15)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.game_over = False

        self.update_score()
        self.place_food()
        self.start_game()


def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()