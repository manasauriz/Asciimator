from ansi import Ansi
import keyboard


class Animator:

    def __init__(self, animation):
        self.anim = animation
        self.W = animation.width
        self.H = animation.height
        self.frame = ""
        self.cur = 0

    def run(self):
        Ansi.hide()
        Ansi.clear()
        keyboard.block_key('enter')

        self.draw_window()
        self.new_frame()

        while True:

            event = keyboard.read_event()
            key = event.name

            if event.event_type == keyboard.KEY_DOWN:
                Ansi.place(self.x, self.y + 1, self.frame[self.index(self.x, self.y + 1)])

                if key == 'esc': 
                    break

                elif key == 'up' and self.y > 2: 
                    self.y -= 1
                elif key == 'down' and self.y < self.H + 1: 
                    self.y += 1
                elif key == 'left' and self.x > 2: 
                    self.x -= 1
                elif key == 'right' and self.x < self.W + 1: 
                    self.x += 1

                elif len(key) == 1:
                    self.add_character(key)
                    if self.x < self.W + 1:
                        self.x += 1
                elif key == 'space' or key == 'backspace' or key == 'delete':
                    self.add_character(" ")
                    if key == 'space' and self.x < self.W + 1:
                        self.x += 1
                elif key == 'shift':
                    second_event = keyboard.read_event()
                    second_key = second_event.name
                    if second_event.event_type == keyboard.KEY_DOWN and len(second_key) == 1:
                        self.add_character(second_key)
                        if self.x < self.W + 1:
                            self.x += 1

                elif key == 'ctrl':
                    second_event = keyboard.read_event()
                    second_key = second_event.name
                    if second_event.event_type == keyboard.KEY_DOWN:
                        if second_key == 'right':
                            self.new_frame()
                        elif second_key == 'left' and 1 < self.cur <= len(self.anim.frames):
                            self.load_frame(self.cur - 2)

                Ansi.place(self.x, self.y + 1, "^")
                
        keyboard.unblock_key('enter')
        Ansi.place(0, self.H + 6)
        Ansi.show()

    def add_character(self, c):
        Ansi.place(self.x, self.y, c)
        i = self.index(self.x, self.y)
        self.frame = self.frame[:i] + c + self.frame[i + 1:]
        self.anim.frames[self.cur - 1] = self.frame

    def draw_window(self):
        Ansi.place(0, self.H + 3, "Press <esc> to exit")
        Ansi.place(0, self.H + 5, "Press <ctrl> + <right> to go to next frame")
        Ansi.place(0, self.H + 6, "Press <ctrl> + <left> to go to next frame")

    def new_frame(self):
        self.frame = ""
        top_bottom = f"+{'-' * self.W}+"
        Ansi.place(1, 1, top_bottom)
        self.frame = top_bottom + "\n"

        middle = "|" + (" " * self.W) + "|"
        for i in range(2, self.H + 2):
            Ansi.place(1, i, middle)
            self.frame += middle + "\n"

        Ansi.place(1, self.H + 2, top_bottom)
        self.x = 2
        self.y = 2
        Ansi.place(self.x, self.y + 1, "^")

        self.frame += top_bottom
        self.anim.frames.append(self.frame)
        self.cur += 1

    def load_frame(self, n):
        self.frame = self.anim.frames[n]
        Ansi.place(1, 1, self.frame)
        self.x = 2
        self.y = 2
        Ansi.place(self.x, self.y + 1, "^")
        self.cur -= 1

    # calculates where index would be in str frame according to current x, y co-ords
    def index(self, x, y):
        return ((self.W + 3) * (y - 1)) + (x - 1)