def clear() -> None:
    """ANSI escape sequence to clear terminal and move cursor to (0,0)"""
    print("\033[2J\033[H", end="")


def hide() -> None:
    """ANSI escape sequence to hide terminal cursor"""
    print("\033[?25l", end="")


def show() -> None:
    """ANSI escape sequence to show terminal cursor"""
    print("\033[?25h", end="")


def place(x = 0, y = 0, text = "", end="\n") -> None:
    """ANSI escape sequence to move cursor to x, y position and/or insert text there"""
    print(f"\033[{y};{x}H{text}", end=end)


def cursor(x = 0, y = 0) -> None:
    """ANSI escape sequence to display a red on screen cursor (^)"""
    print(f"\033[91m\033[{y};{x}H^\033[0m")