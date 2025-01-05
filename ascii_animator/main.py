from .animation import Animation
from . import animator
from . import ansi

import keyboard

import os
import sys
import re
import argparse


def header() -> None:
    """Header logo to be added at the beginning of each menu"""
    ansi.clear()
    logo = f'''
 █████╗ ███████╗ ██████╗██╗██╗    █████╗ ███╗   ██╗██╗███╗   ███╗ █████╗ ████████╗ ██████╗ ██████╗ 
██╔══██╗██╔════╝██╔════╝██║██║   ██╔══██╗████╗  ██║██║████╗ ████║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
███████║███████╗██║     ██║██║   ███████║██╔██╗ ██║██║██╔████╔██║███████║   ██║   ██║   ██║██████╔╝
██╔══██║╚════██║██║     ██║██║   ██╔══██║██║╚██╗██║██║██║╚██╔╝██║██╔══██║   ██║   ██║   ██║██╔══██╗
██║  ██║███████║╚██████╗██║██║   ██║  ██║██║ ╚████║██║██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                  \033[33mA command-line tool to create and run ASCII animations!

____Window Width:{WIN_WIDTH:4} |Window Height:{WIN_HEIGHT:4} |CTRL+C or CTRL+D or CTRL+Z to quit____\033[0m'''
    ansi.place(1, 1, logo)


class DimensionError(Exception):
    """Raised when entered dimension is less than the active terminal window dimensions"""
    pass


class WindowError(Exception):
    """Raise when the selected project cannot be opened in active terminal window"""
    pass


def main() -> None:
    """Entry point for the package. Initializes global variables and parses arguments to redirect them to a relevant menu"""

    parser = argparse.ArgumentParser(description="ASCII Animator Command Line Interface")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--new', action='store_true', help="Start a new project")
    group.add_argument('-l', '--load', action='store_true', help="Load an existing project")
    group.add_argument('-p', '--play', action='store_true', help="Play an animation")
    group.add_argument('-d', '--delete', action='store_true', help="Delete a project")
    args = parser.parse_args()

    os.system("") # This OS command forces current terminal to be compatible with ANSI escape sequences
    global WIN_WIDTH, WIN_HEIGHT
    WIN_WIDTH = get_dimension("width", 500) - 5 # WIN_WIDTH is defined as number of possible characters that can be placed horizontally in current cleared terminal
    WIN_HEIGHT = get_dimension("height", 100) - 5  # WIN_HEIGHT is defined as number of possible characters that can be placed vertically in current cleared terminal
    
    message = ""
    if WIN_WIDTH < 95 or WIN_HEIGHT < 5:
        message += ">> Terminal width must be atleast 95 to run asciimation\n"
        message += ">> Terminal height must be atleast 5 to run asciimation\n"
        message += ">> Resize the terminal and try again\n"
    else:

        try:
            if args.new:
                new_project()
            elif args.load:
                load_project()
            elif args.play:
                play_animation()
            elif args.delete:
                delete_project()
            else:
                main_menu()

        except (EOFError, KeyboardInterrupt):
            message += ">> Quitting...\n"
        except DimensionError:
            message += f">> Width cannot be more than {WIN_WIDTH} in this terminal\n"
            message += f">> Height cannot be more than {WIN_HEIGHT} in this terminal\n"
            message += ">> Enter different dimensions or resize the window and try again\n"
        except WindowError:
            message += ">> Error: This project cannot be opened in this window\n"
            message += ">> Increase terminal size and try again\n"

    header()
    message += "Thank you for using ASCII Animator!"
    keyboard.press_and_release('esc')
    sys.exit(message)


def main_menu() -> None:
    """Main menu that gives access to all functionalities"""
    header()
    print("\033[92mCreate new project |Load existing project |Play animation from saved projects |Delete a project\033[0m")

    ans = input("New Project? (y/N) ").strip().lower()
    yes = ['yes', 'y']
    no = ['no', 'n']

    if ans in yes:
        new_project()
    elif ans in no:
        ans = input("Load Project? (y/N) ").strip().lower()
        if ans in yes:
            load_project()
        elif ans in no:
            ans = input("Play Animation? (y/N) ").strip().lower()
            if ans in yes:
                play_animation()
            elif ans in no:
                ans = input("Delete Project? (y/N) ").strip().lower()
                if ans in yes:
                    delete_project()


def new_project() -> None:
    """Validates name, width and height to create and run a new project using animator"""
    header()
    print("\033[92mCreate a new project\033[0m")

    while True:
        name = input("Enter Project Name: ")
        if re.search(r"^[ 0-9a-zA-Z_\-]+$", name):
            break
        print(">> Error: Invalid name!")
        print(">> Name must contain [a-z], [A-Z], [0-9], '-', '_' or <space>")

    while True:
        try:    
            width = int(input("Enter Frame Width: "))
            if width <= 0:
                raise ValueError
        except ValueError:
            print(">> Error: Enter a valid positve number")
            continue
        if width > WIN_WIDTH:
            raise DimensionError
        break

    while True:
        try:    
            height = int(input("Enter Frame Height: "))
            if height <= 0:
                raise ValueError
        except ValueError:
            print(">> Error: Enter a valid positve number")
            continue
        if height > WIN_HEIGHT:
            raise DimensionError
        break

    movie = Animation(name.strip(), width, height)
    animator.run(movie)


def load_project() -> None:
    """Validates width and height to load and run an existing project using animator"""
    header()
    print("\033[92mLoad an existing project\033[0m")

    if file_path := get_project():
        movie = Animation.load(file_path)
        if movie.width > WIN_WIDTH or movie.height > WIN_HEIGHT:
            raise WindowError
        else:
            animator.run(movie)


def play_animation() -> None:
    """Validates width, height and frame rate to load and play animation for a project"""
    header()
    print("\033[92mPlay animation from saved projects\033[0m")

    if file_path := get_project():
        movie = Animation.load(file_path)
        
        if movie.width > WIN_WIDTH or movie.height > WIN_HEIGHT:
            raise WindowError
        else:
            while True:
                try:
                    frame_rate = int(input("Enter Frame Rate: "))
                    if frame_rate <= 0:
                        raise ValueError
                except ValueError:
                    print(">> Error: Enter a valid positive number!")
                    continue
                break
            movie.play(frame_rate)


def delete_project() -> None:
    """Deletes an exisitng project"""
    header()
    print("\033[92mDelete a project\033[0m")

    if file_path := get_project():
        os.remove(file_path)
        print(">> File deleted successfully!")
        main_menu()
    else:
        print(">> Error: Cannot delete file")


def get_project():
    """
    Displays all projects and returns path to chosen project
    
    Returns:
        str: absolute path to a project file
    """
    all_files = get_all_files()
    for i, file in enumerate(all_files, start=1):
        print(f"Enter {i:2} to select --> {' '.join(file[:-5].split('_')).title()}") # Display an appropriate project name

    while True:
        try:
            file_number = int(input("Enter number: "))
            if file_number <= 0 or file_number > len(all_files):
                raise ValueError
        except ValueError:
            print(f">> Error: Enter a valid number from 1 to {len(all_files)}")
            continue
        break

    current_dir = os.path.dirname(os.path.abspath(__file__)) # Get absolute path to directory running this file
    file_path = os.path.join(current_dir, "projects", all_files[file_number - 1])
    return file_path


def get_all_files():
    """
    Helper function to fetch list of file names for all projects
    
    Returns:
        list: file names of of all projects
    """
    all_files = []
    current_dir = os.path.dirname(os.path.abspath(__file__)) # Get absolute path to directory running this file
    projects_dir = os.path.join(current_dir, "projects")

    for file in os.listdir(projects_dir):
        if file.endswith(".json"):
            all_files.append(file)
    return all_files


def get_dimension(dimension, limit):
    """
    Get width or height (in character spaces) of the terminal running this program using ANSI sequence to get cursor position.

    Args:
        dimension(str): to indicate width or height
        limit(int): coordinate for placing the cursor

    Returns:
        int: width (represented by column) or height (represented by row) or return value of a recursive functional call
    """
    if dimension == "width":
        ansi.place(limit, 1, end="") # Place cursor horizontally at a high number
    elif dimension == "height":
        ansi.place(1, limit, end="") # Place cursor vertically at a high number
    keyboard.press_and_release('enter') # Simulate enter keypress to avoid input blocking by stdin
    print("\033[6n")

    response = ""
    while True:
        char = sys.stdin.read(1)  # Read one character at a time
        response += char
        if char == "R":  # End of ANSI response
            break
    response = response.strip()  # Strip non-visible characters and parse the response
    row, column = map(int, response[2:-1].split(";"))

    if dimension == "width":
        if column < limit: # Return width/ column if cursor position less than limit
            return column
    elif dimension == "height":
        if row < limit: # Return height/ row if cursor position less than limit
            return row 
        
    limit += limit # Double the limit to increase chances of finding end in the next function call
    return get_dimension(dimension, limit)