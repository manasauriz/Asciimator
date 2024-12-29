from animation import Animation
import animator
import ansi
import os
import sys
import keyboard


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
        if not name or name == "":
            print("Error: Invalid name! Try again")
            continue
        try:    
            width = int(input("Enter Frame Width: "))
            height = int(input("Enter Frame Height: "))
            if width <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            print("Error: Enter a valid positve number")
            continue
        if width > WIN_WIDTH - 5 or height > WIN_HEIGHT - 10:
            print(f"Error: Width cannot be more than {WIN_WIDTH - 5} and Height cannot be more than {WIN_HEIGHT - 10}")
            continue
        break

    movie = Animation(name.strip(), width, height)
    animator.run(movie)


def load_project() -> None:
    header()
    print("Load an existing project")

    if file_name := get_project():
        movie = Animation.load(file_name)
        if movie.width > WIN_WIDTH - 5 or movie.height > WIN_HEIGHT - 10:
            print(f"Error: {movie.name} cannot be opened in this window\nResize the terminal and try again.")
        else:
            animator.run(movie)


def play_animation() -> None:
    header()
    print("Play animation from saved projects")

    if file_name := get_project():
        movie = Animation.load(file_name)
        
        if movie.width > WIN_WIDTH - 5 or movie.height > WIN_HEIGHT - 5:
            print(f"Error: {movie.name} cannot be played in this window\nResize the terminal and try again.")
        else:
            while True:
                try:
                    frame_rate = int(input("Enter Frame Rate: "))
                    if frame_rate <= 0:
                        raise ValueError
                except ValueError:
                    print("Error: Enter a valid positive number!")
                    continue
                break
            movie.play(frame_rate)


def delete_project() -> None:
    header()
    print("Delete a project")

    if file_name := get_project():
        if os.path.exists(f"./projects/{file_name}"):
            os.remove(f"./projects/{file_name}")
            print(f"{file_name} deleted successfully!")


def get_project():
    all_files = []
    for file in os.listdir("./projects"):
        if file.endswith(".txt"):
            print(f"--> {" ".join(file[:-4].split("_")).capitalize()}")
            all_files.append(file)

    file_name = "_".join(input("Enter File Name: ").strip().lower().split(" "))
    if not file_name.endswith(".txt"):
        file_name += ".txt"
    return file_name if file_name in all_files else print("Error: Invalid file")


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
    os.system("")
    global WIN_WIDTH, WIN_HEIGHT
    WIN_WIDTH = get_dimension("width", 500)
    WIN_HEIGHT = get_dimension("height", 100)

    argc = len(sys.argv)
    if argc == 1:
        main_menu()
    elif argc == 2:
        cmd = sys.argv[1].strip().lower()
        if cmd in ['n', '-n', 'new', '-new']:
            new_project()
        elif cmd in ['l', '-l', 'load', '-load']:
            load_project()
        elif cmd in ['p', '-p', 'play', '-play']:
            play_animation()
        elif cmd in ['d', '-d', 'del', '-del', 'delete', '-delete']:
            delete_project()