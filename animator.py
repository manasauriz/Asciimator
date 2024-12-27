import ansi
import time
import keyboard
import pygetwindow as gw  


def run(animation) -> None:
    global x, y, frames, width, height, cur
    frames = animation.frames
    width = animation.width
    height = animation.height
    x, y, cur = 2, 2, -1

    window()

    while True:
        keyboard.block_key('enter')
        title = gw.getActiveWindowTitle()
        if not title or 'ASCII_Animator' not in title:
            keyboard.unblock_key('enter')
            time.sleep(0.1)
            continue
        
        ansi.place(x, y + 1, "^")
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

            elif key == 'space' or key == 'backspace' or key == 'delete':
                add_character(" ")
                if key == 'space' and x < width + 1:
                    x += 1
                if key == 'backspace' and x > 2:
                    x -= 1
                    
            elif key == 'shift':
                second_event = keyboard.read_event()
                second_key = second_event.name
                if second_event.event_type == keyboard.KEY_DOWN and len(second_key) == 1:
                    add_character(second_key)
                    if x < width + 1:
                        x += 1

            elif key == 'ctrl':
                second_event = keyboard.read_event()
                second_key = second_event.name
                if second_event.event_type == keyboard.KEY_DOWN:
                    if second_key == 'right':
                        if cur >= len(frames) - 1:
                            new_frame()
                        else:
                            cur += 1
                            ansi.place(1, 1, frames[cur])
                    elif second_key == 'left' and cur > 0:
                        cur -= 1
                        ansi.place(1, 1, frames[cur])
            
                    elif second_key == 'z':
                        global copied
                        copied = frames[cur]
                    elif second_key == 'x' and copied:
                        frames[cur] = copied
                        ansi.place(1, 1, copied)
    animation.save()
    quit()   
        

def window() -> None:
    ansi.hide()
    ansi.clear()
    new_frame()
    ansi.place(0, height + 3, "Press <esc> to exit")
    ansi.place(0, height + 4, "Use <ctrl + z> and <ctrl + x> for copy-pasting frames")
    ansi.place(0, height + 5, "Press <ctrl + right> to go to next frame")
    ansi.place(0, height + 6, "Press <ctrl + left> to go to previous frame")


def quit() -> None:
    keyboard.unblock_key('enter')
    ansi.place(0, height + 6)
    ansi.show()


def new_frame() -> None:
    global cur
    cur += 1
    frames.append("")

    top_bottom = f"+{'-' * width}+"
    ansi.place(1, 1, top_bottom)
    frames[cur] += top_bottom + "\n"

    middle = "|" + (" " * width) + "|"
    for i in range(2, height + 2):
        ansi.place(1, i, middle)
        frames[cur] += middle + "\n"

    ansi.place(1, height + 2, top_bottom)
    frames[cur] += top_bottom


def index(x, y):
    '''calculates where index would be in str frame according to current x, y co-ords'''
    return ((width + 3) * (y - 1)) + (x - 1)


def add_character(c) -> None:
    ansi.place(x, y, c)
    i = index(x, y)
    frames[cur] = frames[cur][:i] + c + frames[cur][i + 1:]