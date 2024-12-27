# clears the terminal
def clear() -> None:
    print("\033[2J\033[H")

# hide the cursor
def hide() -> None:
    print("\033[?25l")

# show the cursor
def show() -> None:
    print("\033[?25h")

# move cursor to x, y position and/or insert text there
def place(x = 0, y = 0, text = "") -> None:
    print(f"\033[{y};{x}H{text}")