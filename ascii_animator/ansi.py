# clears the terminal
def clear() -> None:
    print("\033[2J\033[H", end="")


# hide the cursor
def hide() -> None:
    print("\033[?25l", end="")


# show the cursor
def show() -> None:
    print("\033[?25h", end="")


# move cursor to x, y position and/or insert text there
def place(x = 0, y = 0, text = "", end="\n") -> None:
    print(f"\033[{y};{x}H{text}", end=end)


def cursor(x = 0, y = 0) -> None:
    print(f"\033[91m\033[{y};{x}H^\033[0m")