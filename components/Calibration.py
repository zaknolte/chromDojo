class Calibration:
    def __init__(self, compound) -> None:
        self.compound = compound
        self.points = []

    def add_point(self, point):
        self.points.append(point)
        self.sort_points()

    def delete_point(self, point):
        for p in self.points[::-1]:
            if p.name == point.name:
                del p

    def rename_points(self):
        self.points = self.sort_points()
        for i, point in enumerate(self.points, start=1):
            point.name = f"Cal {i}"

    def sort_points(self):
        self.points = sorted(self.points, lambda x: x.name)

class calPoint:
    def __init__(self, name, x, y) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.used = True

    def set_used(self, use):
        self.used = use