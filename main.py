from animation import Animation
import animator
import ansi
import os
import sys


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


def main_menu() -> None:
    header()
    print("Create a new project | Load an existing project | Play animation from saved projects")

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


def new_project() -> None:
    header()
    print("Create a new project")

    while True:
        try:    
            name = input("Enter Project Name: ")
            if not name or name == "":
                raise ValueError
            width = int(input("Enter Frame Width: "))
            height = int(input("Enter Frame Height: "))
            break
        except ValueError:
            print("Error: Enter a valid name and number!")

    if name.endswith(".txt"):
        name = name[:-4]
    movie = Animation(name.strip().lower(), width, height)
    animator.run(movie)


def load_project() -> None:
    header()
    print("Load an existing project")

    if project := get_project():
        movie = Animation.load(project)
        animator.run(movie)


def play_animation() -> None:
    header()
    print("Play animation from saved projects")

    if project := get_project():
        movie = Animation.load(project)
        try:
            frame_rate = int(input("Enter Frame Rate: "))
        except ValueError:
            pass
        else:
            movie.play(frame_rate)


def get_project():
    all_files = []
    i = 1
    for file in os.listdir("./projects"):
        if file.endswith(".txt"):
            print(f"{i}. {file.capitalize()[:-4]}")
            all_files.append(file)
            i += 1

    file_name = input("Enter File Name: ").strip().lower()
    if not file_name.endswith(".txt"):
        file_name += ".txt"
    return file_name if file_name in all_files else None


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1:
        main_menu()
    elif argc == 2 and sys.argv[1].strip().lower() in ['n', '-n', 'new', '-new']:
        new_project()
    elif argc == 2 and sys.argv[1].strip().lower() in ['l', '-l', 'load', '-load']:
        load_project()
    elif argc == 2 and sys.argv[1].strip().lower() in ['p', '-p', 'play', '-play']:
        play_animation()