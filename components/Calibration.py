class Calibration:
    def __init__(self, compound) -> None:
        self.compound = compound
        self.points = []

    def add_point(self, point):
        self.points.append(point)
        self.sort_points()

    def delete_point(self, level):
        for i, p in enumerate(self.points[::-1]):
            if p.name == level:
                self.points.pop(~i)
        self.sort_points()

    def rename_points(self):
        self.sort_points()
        for i, point in enumerate(self.points, start=1):
            point.name = i

    def sort_points(self):
        self.points = sorted(self.points, key=lambda x: x.name)

class calPoint:
    def __init__(self, name, x, y) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.used = True

    def set_used(self, use):
        self.used = use