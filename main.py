import time
from neopixel import NeoPixel
from machine import Pin
from random import randint

class Snake:
    def __init__(self):
        self.np = NeoPixel(Pin(32), 256)
        self.snake = [[0, 0], [1, 0], [2, 0]]
        self.color = (255, 212, 59)
        self.vx = 1
        self.vy = 0
        self.add_food()

    def set_pixel(self, x, y, color):
        self.np[x + y * 16] = color

    def add_food(self):
        x = randint(0, 64)
        y = randint(0, 8)
        while [x, y] in self.snake:
            x = randint(0, 64)
            y = randint(0, 8)
        self.set_pixel(x, y, (255, 0, 0))

    def move(self):
        new_head = [self.snake[-1][0] + self.vx, self.snake[-1][1] + self.vy]
        if new_head in self.snake:
            return False
        if new_head[0] < 0 or new_head[0] >= 32 or new_head[1] < 0 or new_head[1] >= 8:
            return False
        self.snake.append(new_head)
        if self.np[new_head[0] + new_head[1] * 16] == (255, 0, 0):
            self.add_food()
        else:
            tail = self.snake.pop(0)
            self.set_pixel(tail[0], tail[1], (0, 0, 0))
        for x, y in self.snake:
            self.set_pixel(x, y, self.color)
        return True
    
    def run(self):
        for i in range(100):
            if not self.move():
                break
            self.np.write()
            time.sleep(0.3)


noise = Pin(15, Pin.IN, Pin.PULL_DOWN)    
snakegame = Snake()
snakegame.run()
