import ansi
import time
import json
import os

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
        data = {
            "name": self.name, 
            "width": self.width, 
            "height": self.height, 
            "frames": self.frames
        }

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = "_".join(self.name.lower().split(" ")) + ".json"
        file_path = os.path.join(current_dir, "projects", file_name)

        with open(file_path, 'w') as file:
            json.dump(data, file)
        
    def play(self, frame_rate):
        ansi.hide()
        ansi.clear()
        ansi.place(1, self.height + 3, f"{self.name} @ {frame_rate} FPS")

        for frame in self.frames:
            ansi.place(1, 1, frame)
            time.sleep(1 / frame_rate)
        
        ansi.place(1, self.height + 4)
        ansi.show()


    @classmethod
    def load(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        animation = cls(data["name"], data["width"], data["height"])
        animation.frames = data["frames"]
        return animation