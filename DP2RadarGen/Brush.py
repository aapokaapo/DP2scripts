class Brush:
    def __init__(self, brush_list):
        self.brush = list()

        self.create_brush(brush_list)

    def create_brush(self, brush_list):
        for line in brush_list:
            point = list()
            line = line.split(")")
            line.pop(3)
            for vertex in line:
                vertex = vertex.replace("(", "")
                coordinates = vertex.split(" ")
                coordinate_list = list()
                for coordinate in coordinates:
                    if not len(coordinate) == 0:
                        coordinate_list.append(int(coordinate))
                point.append(coordinate_list)
            self.brush.append(point)
                        # print(coordinate)
                # print(vertex)
        # print(brush_list)