from ink2canvas.svg.Path import Path

class Polygon(Path):
    def getData(self):
        points = self.attr("points").strip().split(" ")
        points = map(lambda x: x.split(","), points)
        comm = []
        for pt in points:           # creating path command similar
            pt = map(float, pt)
            comm.append(["L", pt])
        comm[0][0] = "M"            # first command must be a 'M' => moveTo
        return comm