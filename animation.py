import ansi
import time

class Animation:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height        
        self.frames = [self.clean_frame()]

    def clean_frame(self):
        frame = f"+{'-' * self.width}+\n"
        for i in range(2, self.height + 2):
            frame += f"|{(" " * self.width)}|\n"
        frame += f"+{'-' * self.width}+\n"
        return frame

    def save(self):
        file_name = "_".join(self.name.lower().split(" ")) + ".txt"
        with open(f"./projects/{file_name}", 'w') as file:
            file.write(f"{self.name}\n{self.width}\n{self.height}\n")
            for frame in self.frames:
                file.write(frame)
        
    def play(self, frame_rate):
        ansi.hide()
        ansi.clear()
        fname = self.name if len(self.name) <= 10 else self.name[:7] + "..."
        ansi.place(1, self.height + 3, f"{fname:10} ({frame_rate} FPS)")

        for frame in self.frames:
            ansi.place(1, 1, frame)
            time.sleep(1 / frame_rate)
        
        fname = self.name if len(self.name) <= 10 else self.name[:7] + "..."
        ansi.place(1, self.height + 4)
        ansi.show()

    @classmethod
    def load(cls, file_name):
        with open(f"./projects/{file_name}", 'r') as file:
            name = file.readline().strip()
            width = int(file.readline().strip())
            height = int(file.readline().strip())
            animation = cls(name, width, height)

            frames = []
            frame = ""
            cur = 0
            for line in file.readlines():
                if cur < height + 2:
                    frame += line
                    cur += 1
                else:
                    frames.append(frame)
                    frame = line
                    cur = 1
            frames.append(frame)

            animation.frames = frames
            return animation