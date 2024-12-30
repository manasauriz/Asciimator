from animation import Animation
import animator
import ansi
import os
import sys
import keyboard
import argparse
import re


def header() -> None:
    ansi.clear()
    logo = '''
 █████╗ ███████╗ ██████╗██╗██╗    █████╗ ███╗   ██╗██╗███╗   ███╗ █████╗ ████████╗ ██████╗ ██████╗ 
██╔══██╗██╔════╝██╔════╝██║██║   ██╔══██╗████╗  ██║██║████╗ ████║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
███████║███████╗██║     ██║██║   ███████║██╔██╗ ██║██║██╔████╔██║███████║   ██║   ██║   ██║██████╔╝
██╔══██║╚════██║██║     ██║██║   ██╔══██║██║╚██╗██║██║██║╚██╔╝██║██╔══██║   ██║   ██║   ██║██╔══██╗
██║  ██║███████║╚██████╗██║██║   ██║  ██║██║ ╚████║██║██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
Make cool ascii animations!
'''
    ansi.place(1, 1, logo)
    print(f"Current Window Width:{WIN_WIDTH:4} |Current Window Height: {WIN_HEIGHT:4}")


def main() -> None:

    parser = argparse.ArgumentParser(description="ASCII Animator Command Line Interface")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--new', action='store_true', help="Start a new project")
    group.add_argument('-l', '--load', action='store_true', help="Load an existing project")
    group.add_argument('-p', '--play', action='store_true', help="Play an animation")
    group.add_argument('-d', '--delete', action='store_true', help="Delete a project")

    args = parser.parse_args()
    os.system("")
    global WIN_WIDTH, WIN_HEIGHT
    WIN_WIDTH = get_dimension("width", 500)
    WIN_HEIGHT = get_dimension("height", 100)

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


def main_menu() -> None:
    header()
    print("Create a new project | Load an existing project | Play animation from saved projects | Delete a project")

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
                elif ans in no:
                    ...


def new_project() -> None:
    header()
    print("Create a new project")

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
        if width > WIN_WIDTH - 5:
            print(f">> Error: Width cannot be more than {WIN_WIDTH - 5}")
            print(">> Enter different dimensions or resize the window and try again")
            continue
        break
    while True:
        try:    
            height = int(input("Enter Frame Height: "))
            if height <= 0:
                raise ValueError
        except ValueError:
            print(">> Error: Enter a valid positve number")
            continue
        if height > WIN_HEIGHT - 10:
            print(f">> Error: Height cannot be more than {WIN_HEIGHT - 10}")
            print(">> Enter different dimensions or resize the window and try again")
            continue
        break

    movie = Animation(name.strip(), width, height)
    animator.run(movie)


def load_project() -> None:
    header()
    print("Load an existing project")

    if file_path := get_project():
        movie = Animation.load(file_path)
        if movie.width > WIN_WIDTH - 5 or movie.height > WIN_HEIGHT - 10:
            print(f">> Error: {movie.name} cannot be opened in this window")
            print(">> Increase terminal size and try again")
        else:
            animator.run(movie)


def play_animation() -> None:
    header()
    print("Play animation from saved projects")

    if file_path := get_project():
        movie = Animation.load(file_path)
        
        if movie.width > WIN_WIDTH - 5 or movie.height > WIN_HEIGHT - 5:
            print(f">> Error: {movie.name} cannot be played in this window")
            print(">> Increase terminal size and try again")
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
    header()
    print("Delete a project")

    if file_path := get_project():
        os.remove(file_path)
        print(">> File deleted successfully!")
        main_menu()
    else:
        print(">> Error: Cannot delete file")


def get_project():
    all_files = get_all_files()
    for i, file in enumerate(all_files, start=1):
        print(f"Enter {i:2} to select --> {" ".join(file[:-5].split("_")).title()}")

    while True:
        try:
            file_number = int(input("Enter number: "))
            if file_number <= 0 or file_number > len(all_files):
                raise ValueError
        except ValueError:
            print(f">> Error: Enter a valid number from 1 to {len(all_files)}")
            continue
        break

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "projects", all_files[file_number - 1])
    return file_path


def get_all_files():
    all_files = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    projects_dir = os.path.join(current_dir, "projects")

    for file in os.listdir(projects_dir):
        if file.endswith(".json"):
            all_files.append(file)
    return all_files


def get_dimension(dimension, limit):
    if dimension == "width":
        ansi.place(limit, 1, end="")
    elif dimension == "height":
        ansi.place(1, limit, end="")
    keyboard.press_and_release('enter')
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
        if column < limit:
            return column
    elif dimension == "height":
        if row < limit:
            return row
        
    limit += limit
    return get_dimension(dimension, limit)


if __name__ == "__main__":
    main()