from animation import Animation
from animator import Animator

if __name__ == "__main__":
    movie = Animation(50, 10)
    app = Animator(movie)
    app.run()

    for frame in movie.frames:
        print(frame)
        print()