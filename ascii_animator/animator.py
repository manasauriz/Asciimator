from . import ansi

import keyboard
import pygetwindow as gw
import pyperclip as clip

import time


CONTROLS = '''\033[92m_____CONTROLS: Press ESC to quit & use ARROW KEYS to move_____\033[0m
\033[33mTAB + S\033[0m -- save animation  |\033[33mTAB + N\033[0m -- add new frame next to current frame
\033[33mTAB + P\033[0m -- play animation  |\033[33mTAB + M\033[0m -- add a copy of current frame next to it  
\033[33mTAB + >\033[0m -- load next frame |\033[33mTAB + BACKSPACE\033[0m   -- wipes current frame
\033[33mTAB + <\033[0m -- load prev frame |\033[33mTAB + DELETE or D\033[0m -- delete current frame
'''


def run(animation) -> None:
    """
    Initialize animator window, set up global variables, check if terminal is active and controls for various keyboard events

    Keyboard Events and Controls:
        esc: save and quit program
        arrow keys: move cursor around frame
        character key: add character on screen and move cursor forward
        shift + character key: add alternate version of character on screen and move cursor forward
        space: add whitespace character on screen and move cursor forward
        backspace: add whitespace character on screen and move cursor backward
        delete: add whitespace character on screen without moving cursor
        ctrl + v: add copied characters on screen, as much as a line can fit
        tab + s: save current progress in file
        tab + p: play animation of current progress
        tab + right or '>' -> load next frame
        tab + left or '<' -> load previous frame
        tab + n -> add new frame next to current frame
        tab + m -> copy current frame and add copied frame next to current frame
        tab + backspace -> wipes current frame
        tab + d or delete -> delete current frame data
    """
    global name, width, height, frames, cur, x, y
    name = animation.name
    width = animation.width
    height = animation.height
    frames = animation.frames
    cur = len(frames) - 1 # Represents current active frame
    x, y = 2, 2 # Represent current coordinated in frame

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

                elif key == 'up' and y > 2: 
                    y -= 1
                elif key == 'down' and y < height + 1: 
                    y += 1
                elif key == 'left' and x > 2: 
                    x -= 1
                elif key == 'right' and x < width + 1: 
                    x += 1

                elif len(key) == 1:
                    add_character(key)
                    if x < width + 1:
                        x += 1
                elif key == 'shift':
                    second_event = keyboard.read_event()
                    second_key = second_event.name
                    if second_event.event_type == keyboard.KEY_DOWN and len(second_key) == 1:
                        add_character(second_key)
                        if x < width + 1:
                            x += 1

                elif key == 'space':
                    add_character(" ")
                    if x < width + 1:
                        x += 1
                elif key == 'backspace':
                    add_character(" ")
                    if x > 2:
                        x -= 1
                elif key == 'delete':
                    add_character(" ")

                elif key == 'ctrl':
                    second_event = keyboard.read_event()
                    second_key = second_event.name
                    if second_event.event_type == keyboard.KEY_DOWN and second_key in ['v', 'V']:
                            text = clip.paste()
                            for c in text:
                                add_character(c)
                                if x < width + 1:
                                    x += 1
                                else:
                                    break

                elif key == 'tab':
                    second_event = keyboard.read_event()
                    second_key = second_event.name
                    if second_event.event_type == keyboard.KEY_DOWN:

                        if second_key in ['s', 'S']:
                            animation.frames = frames
                            animation.save()
                        elif second_key in ['p', 'P']:
                            animation.frames = frames
                            animation.play(get_frame_rate())
                            load_window()

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
                        elif second_key in ['m', 'M']:
                            copied = frames[cur]
                            cur += 1
                            frames = frames[:cur] + [copied] + frames[cur:]
                            load_frame()

                        elif second_key == 'backspace':
                            frames[cur] = animation.clean_frame()
                            load_frame()
                        elif second_key in ['d', 'D', 'delete']:
                            frames = frames[:cur] + frames[cur + 1:]
                            cur -= 1
                            load_frame()

    animation.frames = frames
    animation.save()
    if blocked:
        blocked = False
        block_controls(blocked)
    ansi.place(1, height + 8)
    ansi.show()


def load_frame() -> None:
    """Display current frame and info related to it"""
    ansi.place(1, 1, frames[cur])
    fname = name if len(name) <= 20 else name[:17] + "..."
    frame_info = f"\033[33mCURRENT FRAME:\033[0m{cur + 1:4} |\033[33mTOTAL FRAMES:\033[0m{len(frames):4} |\033[33m{fname:20}\033[0m ({width} X {height})"
    ansi.place(1, height + 3, frame_info)


def load_window() -> None:
    """Initialize window on screen and display frame and controls"""
    ansi.hide()
    ansi.clear()
    load_frame()
    ansi.place(1, height + 4, CONTROLS)


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


def get_frame_rate():
    """
    Clear display and get frame rate from user to play animation

    Returns:
        int: frame rate for animation
    """
    ansi.show()
    keyboard.unblock_key('enter')
    keyboard.press_and_release('enter')
    while True:
        try:
            ansi.clear()
            frame_rate = int(input("Enter Frame Rate: "))
            break
        except ValueError:
            pass
    keyboard.block_key('enter')
    ansi.hide()
    return frame_rate