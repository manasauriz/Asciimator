from . import ansi

import time
import json
import os

class Animation:
    """
    A class that represents an animation project. It holds metadata to interact with ASCII Animations in terminal

    Attributes:
        name(str): Name of the project
        width(int): Width of a frame (in characters)
        height(int): Height of a frame (in characters)
        frames(list): Collection of strings, each representing a frame
    """

    def __init__(self, name, width, height):
        """
        Initialize an Animation object and assign a single empty frame to frames

        Parameters:
            name(str): Name of the project
            width(int): Width of a frame (in characters)
            height(int): Height of a frame (in characters)
        """
        self.name = name
        self.width = width
        self.height = height        
        self.frames = [self.clean_frame()]

    def clean_frame(self):
        """
        Create a string representation of an empty frame with specific dimensions

        Returns:
            str: empty frame
        """
        frame = f"+{'-' * self.width}+\n"
        for i in range(2, self.height + 2):
            frame += f"|{(' ' * self.width)}|\n"
        frame += f"+{'-' * self.width}+\n"
        return frame

    def save(self):
        """Saves current project's state in a JSON file"""
        data = {
            "name": self.name, 
            "width": self.width, 
            "height": self.height, 
            "frames": self.frames
        }

        current_dir = os.path.dirname(os.path.abspath(__file__)) # Get absolute path to directory running this file
        file_name = "_".join(self.name.lower().split(" ")) + ".json" # Generate an appropriate file name 
        file_path = os.path.join(current_dir, "projects", file_name)

        with open(file_path, 'w') as file:
            json.dump(data, file)
        
    def play(self, frame_rate):
        """
        Consecutively print frames on screen at a particular frame rate to simulate animation

        Parameters:
            frame_rate(int): frame rate for animation
        """
        ansi.hide()
        ansi.clear()
        ansi.place(1, self.height + 3, f"\033[33m{self.name} @ {frame_rate} FPS\033[0m")

        for frame in self.frames:
            ansi.place(1, 1, frame)
            time.sleep(1 / frame_rate)
        time.sleep(1)
        
        ansi.place(1, self.height + 5)
        ansi.show()


    @classmethod
    def load(cls, file_path):
        """
        Generate an Animation object using an appropriate JSON project file

        Parameters:
            file_path(str): absolute path to a project file

        Returns:
            Animation: Animation object created using JSON project file
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        animation = cls(data["name"], data["width"], data["height"])
        animation.frames = data["frames"]
        return animation