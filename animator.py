import ansi
import time
import keyboard
import pygetwindow as gw
import pyperclip as clip


CONTROLS = '''_____CONTROLS: Press ESC to quit & use ARROW KEYS to move_____
TAB + S -- save animation  |TAB + N -- add new frame next to current frame
TAB + P -- play animation  |TAB + M -- add a copy of current frame next to it  
TAB + > -- load next frame |TAB + BACKSPACE   -- wipes current frame
TAB + < -- load prev frame |TAB + DELETE or D -- delete current frame
'''
'''
esc -> save and quit program
up -> moves cursor up
down -> moves cursor down
right -> moves cursor right
left -> moves cursor left
character -> adds the character and moves cursor forward
shift + character -> adds alternate version of character and moves cursor forward
space -> adds whitespace and moves cursor forward
backspace -> adds whitespace and moves cursor backward
delete -> adds whitespace without moving cursor
tab + s -> save current progress in file
tab + p -> animate current progress
tab + v -> paste copied character from clipboard
tab + right -> load next frame
tab + left -> load previous frame
tab + n -> add new frame next to current frame
tab + c -> copy current frame and add copied frame next to current frame
tab + backspace -> wipes current frame
tab + d or ctrl + delete -> delete current frame data
'''


def run(animation) -> None:
    global name, width, height, frames, cur, x, y
    name = animation.name
    width = animation.width
    height = animation.height
    frames = animation.frames
    cur = len(frames) - 1
    x, y = 2, 2

    load_window()   
    title = gw.getActiveWindowTitle()
    blocked = False

    while True:
        new_title = gw.getActiveWindowTitle()
        if not new_title or (new_title not in title) or (title not in new_title):
            if blocked:
                blocked = False
                block_controls(blocked)
            time.sleep(0.1)
            continue
        else:
            if not blocked:
                blocked = True
                block_controls(blocked)
                
            ansi.cursor(x, y + 1)
            event = keyboard.read_event()
            key = event.name
            if event.event_type == keyboard.KEY_DOWN:
                ansi.place(x, y + 1, frames[cur][index(x, y + 1)])

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
    ansi.place(1, height + 8)
    ansi.show()
    if blocked:
        blocked = False
        block_controls(blocked)


def load_frame() -> None:
    ansi.place(1, 1, frames[cur])
    fname = name if len(name) <= 10 else name[:7] + "..."
    frame_info = f"CURRENT FRAME:{cur + 1:4} |TOTAL FRAMES:{len(frames):4} |{fname:10} ({width} X {height})"
    ansi.place(1, height + 3, frame_info)


def load_window() -> None:
    ansi.hide()
    ansi.clear()
    load_frame()
    ansi.place(1, height + 4, CONTROLS)


def index(x, y):
    '''calculates where index would be in str frame according to current x, y co-ords'''
    return ((width + 3) * (y - 1)) + (x - 1)


def add_character(c) -> None:
    ansi.place(x, y, c)
    i = index(x, y)
    frames[cur] = frames[cur][:i] + c + frames[cur][i + 1:]


def block_controls(flag):
    keys = ['enter']
    if flag:
        for key in keys:
            keyboard.block_key(key)
    else:
        for key in keys:
            keyboard.unblock_key(key)


def get_frame_rate():
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