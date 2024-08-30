class Area:
    def __init__(self, x=0, y=0, size=0):
        self.x = x
        self.y = y
        self.size = size

    def set(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def get_position(self):
        return self.x, self.y

    def get_size(self):
        return self.size

