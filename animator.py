import ansi
import time
import keyboard
import pygetwindow as gw
import pyperclip as clip


def run(animation) -> None:
    global width, height, frames, cur, x, y
    width = animation.width
    height = animation.height
    frames = animation.frames
    cur = len(frames) - 1
    x, y = 2, 2

    load_window()   
    
    blocked = True
    while True:
        title = gw.getActiveWindowTitle()
        if not title or 'ASCII_Animator' not in title:
            if blocked:
                keyboard.unblock_key('enter')
                blocked = False
            time.sleep(0.25)
            continue
        if not blocked:
            keyboard.block_key('enter')
        
        ansi.place(x, y + 1, "^")
        event = keyboard.read_event()
        key = event.name
        '''
        CONTROLS
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
        ctrl + s -> save current progress in file
        ctrl + a -> animate current progress
        ctrl + p -> paste copied character from clipboard
        ctrl + right -> load next frame
        ctrl + left -> load previous frame
        ctrl + n -> add new frame next to current frame
        ctrl + m -> copy current frame and add copied frame next to current frame
        ctrl + backspace -> wipes current frame
        ctrl + d or ctrl + delete -> delete current frame data
        '''

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
                block_controls(True)
                second_event = keyboard.read_event()
                second_key = second_event.name
                if second_event.event_type == keyboard.KEY_DOWN:

                    if second_key in ['s', 'S']:
                        animation.frames = frames
                        animation.save()
                    elif second_key in ['a', 'A']:
                        animation.frames = frames
                        animation.play(3)
                        load_window()
                    elif second_key in ['p', 'P']:
                        text = clip.paste()
                        for c in text:
                            add_character(c)
                            if x < width + 1:
                                x += 1
                            else:
                                break

                    elif second_key == 'right' and cur < len(frames) - 1:
                        cur += 1
                        load_frame()
                    elif second_key == 'left' and cur > 0:
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

                block_controls(False)
    animation.frames = frames
    animation.save()
    quit()   
        

def load_window() -> None:
    keyboard.block_key('enter')
    ansi.hide()
    ansi.clear()
    load_frame()
    ansi.place(0, height + 3, "Press <esc> to exit")
    ansi.place(0, height + 4, "Use <ctrl + z> and <ctrl + x> for copy-pasting frames")
    ansi.place(0, height + 5, "Press <ctrl + right> to go to next frame, <ctrl + left> to go to previous frame")


def quit() -> None:
    ansi.place(0, height + 6)
    ansi.show()
    keyboard.unblock_key('enter')


def load_frame() -> None:
    ansi.place(1, 1, frames[cur])
    ansi.place(0, height + 6, f"Current Frame: {cur + 1:4}")


def index(x, y):
    '''calculates where index would be in str frame according to current x, y co-ords'''
    return ((width + 3) * (y - 1)) + (x - 1)


def add_character(c) -> None:
    ansi.place(x, y, c)
    i = index(x, y)
    frames[cur] = frames[cur][:i] + c + frames[cur][i + 1:]


def block_controls(flag):
    keys = ['c', 'C', 'x', 'X', 'v', 'V', 'z', 'Z', 'y', 'Y', 
            'f', 'F', 't', 'T', 'w', 'W', '`', '~', 
            'shift', 'tab']
    if flag:
        for key in keys:
            keyboard.block_key(key)
    else:
        for key in keys:
            keyboard.unblock_key(key)