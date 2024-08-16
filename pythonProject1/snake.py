import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()

        self.score = 0
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=('Arial', 14))
        self.score_label.pack()

        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.snake_direction = "Down"
        self.food = None

        self.game_speed = 100
        self.game_running = True

        self.create_objects()
        self.bind_keys()
        self.move_snake()

    def create_objects(self):
        self.snake_body = []
        for x, y in self.snake:
            self.snake_body.append(self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green"))

        self.create_food()

    def create_food(self):
        if self.food:
            self.canvas.delete(self.food)

        x = random.randint(0, 39) * 10
        y = random.randint(0, 39) * 10

        self.food = self.canvas.create_oval(x, y, x + 10, y + 10, fill="red")

    def bind_keys(self):
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))

    def change_direction(self, new_direction):
        all_directions = ["Up", "Down", "Left", "Right"]
        opposites = [{"Up", "Down"}, {"Left", "Right"}]

        if new_direction in all_directions and {new_direction, self.snake_direction} not in opposites:
            self.snake_direction = new_direction

    def move_snake(self):
        if not self.game_running:
            return

        head_x, head_y = self.snake[-1]

        if self.snake_direction == "Up":
            head_y -= 10
        elif self.snake_direction == "Down":
            head_y += 10
        elif self.snake_direction == "Left":
            head_x -= 10
        elif self.snake_direction == "Right":
            head_x += 10

        new_head = (head_x, head_y)

        if self.check_collisions(new_head):
            self.game_over()
            return

        self.snake.append(new_head)
        self.snake_body.append(self.canvas.create_rectangle(head_x, head_y, head_x + 10, head_y + 10, fill="green"))

        if self.check_food_collision(new_head):
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.create_food()
        else:
            self.canvas.delete(self.snake_body.pop(0))
            self.snake.pop(0)

        self.root.after(self.game_speed, self.move_snake)

    def check_collisions(self, new_head):
        x, y = new_head

        if x < 0 or x >= 400 or y < 0 or y >= 400:
            return True

        if new_head in self.snake:
            return True

        return False

    def check_food_collision(self, head):
        food_coords = self.canvas.coords(self.food)
        return food_coords[0] == head[0] and food_coords[1] == head[1]

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(200, 200, text="Game Over", fill="white", font=('Arial', 24))
        self.create_replay_button()

    def create_replay_button(self):
        self.replay_button = tk.Button(self.root, text="Replay", command=self.reset_game, font=('Arial', 14))
        self.replay_button.pack()

    def reset_game(self):
        self.canvas.delete("all")
        self.replay_button.destroy()

        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")

        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.snake_direction = "Down"
        self.food = None

        self.game_running = True

        self.create_objects()
        self.move_snake()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
