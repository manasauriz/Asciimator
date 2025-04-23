from . import ansi

import keyboard
import pygetwindow as gw
import pyperclip as clip

import time
from enum import Enum


class Move(Enum):
    """Enum class to represent movement on screen"""
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def run(animation) -> None:
    """
    Initialize animator window, set up global variables, check if terminal is active and controls for various keyboard events

    Args:
        animation(Animation) - Animation object

    Keyboard Events and Controls:
        esc: save and quit program
        arrow keys: move cursor around frame
        character key: add character on screen and move cursor forward
        shift + character key: add alternate version of character on screen and move cursor forward
        space: add whitespace character on screen and move cursor forward
        backspace: remove previous character and move cursor backward
        delete: remove character on current cursor
        ctrl + v: add copied characters on screen, as much as a line can fit
        alt: display all controls in frame for some time
        tab + s: save current progress in file
        tab + p: play animation of current progress
        tab + f: go to frame
        tab + right or '>': load next frame
        tab + left or '<': load previous frame
        tab + n: add new frame next to current frame
        tab + m: copy current frame and add copied frame next to current frame
        tab + backspace: wipes current frame
        tab + d or delete: delete current frame data
        tab + c: copy current frame data
        tab + v: paste copied frame data onto current frame
    """
    global name, width, height, frames, cur, x, y
    name = animation.name
    width = animation.width
    height = animation.height
    frames = animation.frames
    cur = len(frames) - 1 # Represents current active frame
    x, y = 2, 2 # Represent current coordinated in frame

    def move(movement):
        global x, y
        if movement == Move.UP and y > 2:
            y -= 1
        elif movement == Move.DOWN and y < height + 1:
            y += 1
        elif movement == Move.LEFT  and x > 2:
            x -= 1
        elif movement == Move.RIGHT  and x < width + 1:
            x += 1
        ansi.clear_and_place(height + 5, f"\033[33mCurrent Coordinates (x, y):\033[0m ({x - 1}, {y - 1})")

    load_window()  
    title = gw.getActiveWindowTitle()
    blocked = False

    while True:
        new_title = gw.getActiveWindowTitle()
        if not new_title or (new_title not in title) or (title not in new_title): # If current window is not the terminal program started running in
            if blocked:
                blocked = False
                block_controls(blocked)
            time.sleep(0.1)
            continue
        else: # If current window is the terminal program started running in
            if not blocked:
                blocked = True
                block_controls(blocked)
                
            ansi.cursor(x, y + 1) # Place cursor below current coordinates
            event = keyboard.read_event()
            key = event.name
            if event.event_type == keyboard.KEY_DOWN:
                ansi.place(x, y + 1, frames[cur][index(x, y + 1)]) # Restore previous character at cursor's place

                if key == 'esc': 
                    break

                elif key == 'up': 
                    move(Move.UP)
                elif key == 'down': 
                    move(Move.DOWN)
                elif key == 'left': 
                    move(Move.LEFT)
                elif key == 'right': 
                    move(Move.RIGHT)

                elif len(key) == 1:
                    add_character(key)
                    move(Move.RIGHT)
                elif key == 'shift':
                    second_event = keyboard.read_event()
                    second_key = second_event.name
                    if second_event.event_type == keyboard.KEY_DOWN and len(second_key) == 1:
                        add_character(second_key)
                        move(Move.RIGHT)

                elif key == 'space':
                    add_character(" ")
                    move(Move.RIGHT)
                elif key == 'backspace':
                    move(Move.LEFT)
                    add_character(" ")
                elif key == 'delete':
                    add_character(" ")

                elif key == 'ctrl':
                    second_event = keyboard.read_event()
                    second_key = second_event.name
                    if second_event.event_type == keyboard.KEY_DOWN and second_key in ['v', 'V']:
                            text = clip.paste()
                            for c in text:
                                add_character(c)
                                move(Move.RIGHT)
                                if x > width:
                                    break
                
                elif key == 'alt':
                    load_controls()
                    time.sleep(5)
                    load_window()

                elif key == 'tab':
                    second_event = keyboard.read_event()
                    second_key = second_event.name
                    if second_event.event_type == keyboard.KEY_DOWN:

                        if second_key in ['s', 'S']:
                            animation.frames = frames
                            animation.save()
                            ansi.clear_and_place(height + 5, "Last operation: Saved current progress.")

                        elif second_key in ['p', 'P']:
                            animation.frames = frames
                            animation.play(get_nat_num("Enter Frame Rate: "))
                            load_window()
                        elif second_key in ['f', 'F']:
                            pos = get_nat_num("Where to? (Frame Number): ")
                            cur = len(frames) - 1 if pos > len(frames) else pos - 1
                            load_frame()

                        elif second_key in ['right', '.', '>'] and cur < len(frames) - 1:
                            cur += 1
                            load_frame()
                        elif second_key in ['left', ',', '<'] and cur > 0:
                            cur -= 1
                            load_frame()
                
                        elif second_key in ['n', 'N']:
                            cur += 1
                            frames = frames[:cur] + [animation.clean_frame()] + frames[cur:]
                            load_frame()
                            ansi.clear_and_place(height + 5, "Last operation: Added brand new frame.")
                        elif second_key in ['m', 'M']:
                            current = frames[cur]
                            cur += 1
                            frames = frames[:cur] + [current] + frames[cur:]
                            load_frame()
                            ansi.clear_and_place(height + 5, "Last operation: Duplicated previous frame.")

                        elif second_key == 'backspace':
                            frames[cur] = animation.clean_frame()
                            load_frame()
                            ansi.clear_and_place(height + 5, "Last operation: Cleared frame contents")
                        elif second_key in ['d', 'D', 'delete'] and cur > 0:
                            frames = frames[:cur] + frames[cur + 1:]
                            cur -= 1
                            load_frame()
                            ansi.clear_and_place(height + 5, f"Last operation: Deleted frame {cur + 2}")
                        
                        elif second_key in ['c', 'C']:
                            copied = frames[cur]
                            ansi.clear_and_place(height + 5, f"Last operation: Copied frame {cur + 1}")
                        elif second_key in ['v', 'V']:
                            if copied:
                                frames[cur] = copied
                                load_frame()
                                ansi.clear_and_place(height + 5, f"Last operation: Pasted copied frame to frame {cur + 1}")

    animation.frames = frames
    animation.save()
    if blocked:
        blocked = False
        block_controls(blocked)
    ansi.place(1, height + 5)
    ansi.show()


def load_frame() -> None:
    """Display current frame and info related to it"""
    ansi.place(1, 1, frames[cur])
    fname = name if len(name) <= 20 else name[:17] + "..."
    frame_info = f"\033[33mCURRENT FRAME:\033[0m{cur + 1:4} |\033[33mTOTAL FRAMES:\033[0m{len(frames):4} |\033[33m{fname:20}\033[0m ({width} X {height})"
    ansi.clear_and_place(height + 3, frame_info)


def load_controls() -> None:
    """Displays all controls on screen"""
    CONTROLS = {
        "TAB + S": "save animation", "TAB + P": "play animation", "TAB + F": "go to frame", 
        "TAB + RIGHT or >": "load next frame", "TAB + LEFT or <": "load prev frame", 
        "TAB + N": "add new frame next to current frame", "TAB + M": "add a copy of current frame next to it", 
        "TAB + BACKSPACE": "wipes current frame", "TAB + DELETE or D": "delete current frame", 
        "TAB + C": "copy current frame data", "TAB + V": "paste copied frame data onto current frame"
    }
    control_frame = "\033[92mCONTROLS:\033[0m\n"

    if height < len(CONTROLS):
        controls_list = list(CONTROLS)
        for i in range(3):
            control_frame += f"\033[33m{controls_list[i]:11}:\033[0m {CONTROLS[controls_list[i]]:22}"
        control_frame += "\n"
        for i in range(3, len(controls_list), 2):
            for j in range(i, i + 2):
                detail = CONTROLS[controls_list[j]] if len(CONTROLS[controls_list[j]]) <= 30 else CONTROLS[controls_list[j]][:27] + "..."
                control_frame += f"\033[33m{controls_list[j]:20}:\033[0m {detail:30}"
            control_frame += "\n"

    else:
        for control, detail in CONTROLS.items():
            control_frame += f"\033[33m{control:20}:\033[0m {detail}\n"

    ansi.clear()
    ansi.place(1, 1, control_frame)


def load_window() -> None:
    """Initialize window on screen and display frame and controls"""
    ansi.hide()
    ansi.clear()
    load_frame()
    ansi.clear_and_place(height + 4, "\033[92m__Press ESC to quit |Use ARROW KEYS to move |Press ALT for all Controls__\033[0m")


def index(x, y):
    """
    Calculate where index would be in frame string according to current x, y co-ords
    
    Args:
        x(int): current x coordinate
        y(int): current y coordinate

    Returns:
        int: index in frame string
    """
    return ((width + 3) * (y - 1)) + (x - 1)


def add_character(c) -> None:
    """
    Add character on screen and in frame at current x, y coordinates
    
    Args:
        c(str): character string to be added
    """
    ansi.place(x, y, c)
    i = index(x, y)
    frames[cur] = frames[cur][:i] + c + frames[cur][i + 1:]


def block_controls(flag) -> None:
    """
    Toggle blocking of certain keys like enter that can hinder program execution

    Args:
        flag(bool): True indicates block, False indicates unblock
    """
    keys = ['enter']
    if flag:
        for key in keys:
            keyboard.block_key(key)
    else:
        for key in keys:
            keyboard.unblock_key(key)


def get_nat_num(prompt = "number"):
    """
    Gets a natural number from user while the animator is running

    Returns:
        int: positive integer
    """
    keyboard.unblock_key('enter')
    keyboard.press_and_release('enter') # clears the 'residue'
    while True:
        try:
            ansi.clear_and_place(height + 5)
            number = int(input(prompt))
            if number < 1:
                raise ValueError
            break
        except ValueError:
            pass
    ansi.clear_and_place(height + 5)
    keyboard.block_key('enter')
    return number