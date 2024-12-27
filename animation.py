class Animation:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.frames = []

    def save(self):
        with open(f"{self.name}.txt", "w") as file:
            file.write(f"{self.name}\n{self.width}\n{self.height}\n")
            for frame in self.frames:
                file.write(frame+"\n")

    @classmethod
    def load(cls, file_name):
        with open(file_name, "r") as file:
            name = file.readline().strip()
            width = int(file.readline().strip())
            height = int(file.readline().strip())
            animation = cls(name, width, height)

            frame = ""
            cur = 0
            for line in file.readlines():
                if cur < height + 2:
                    frame += line
                    cur += 1
                else:
                    animation.frames.append(frame)
                    frame = line
                    cur = 1
            animation.frames.append(frame)

            return animation