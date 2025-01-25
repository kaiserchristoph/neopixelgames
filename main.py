import time
from neopixel import NeoPixel
from machine import Pin
from random import randint
import wifi_config

async def bluetooth_scan():
    import aioble
    async with aioble.scan(duration_ms=5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            print(result, result.name(), result.rssi, result.services())


def connect_wifi():
    import network
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(False)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifi_config.ssid, wifi_config.password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ipconfig('addr4'))

class Snake:
    def __init__(self):
        self.np = NeoPixel(Pin(32), 256)
        self.snake = [[0, 7], [1, 7], [2, 7]]
        self.color = (255, 212, 59)
        self.vx = 1
        self.vy = 0
        self.add_food()

    def set_pixel(self, x, y, color):
        if y % 2 == 0:
            index = x + y * 32
        else:
            index = (y + 1) * 32 - 1 - x
        self.np[index] = color

    def get_pixel_color(self, x, y):
        if y % 2 == 0:
            index = x + y * 32
        else:
            index = (y + 1) * 32 - 1 - x
        return self.np[index]

    def add_food(self):
        x = randint(0, 31)
        y = randint(0, 7)
        x = 6
        y = 7
        while [x, y] in self.snake:
            x = randint(0, 31)
            y = randint(0, 7)
        self.set_pixel(x, y, (255, 0, 0))

    def move(self):
        new_head = [self.snake[-1][0] + self.vx, self.snake[-1][1] + self.vy]
        if new_head in self.snake:
            return False
        if new_head[0] < 0 or new_head[0] >= 32 or new_head[1] < 0 or new_head[1] >= 8:
            return False
        self.snake.append(new_head)
        if self.get_pixel_color(new_head[0], new_head[1]) == (255, 0, 0):
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
connect_wifi()
bluetooth_scan()
snakegame = Snake()
snakegame.run()
