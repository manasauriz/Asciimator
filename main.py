from animation import Animation
import animator

if __name__ == "__main__":
    movie = Animation(50, 10)
    animator.run(movie)

    for frame in movie.frames:
        print(frame)
        print()