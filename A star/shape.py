import collis


class Line:
    def __init__(self, points: list) -> None:
        '''
        ex:[[5,6],[7,8]]
        '''
        if(len(points) != 2):
            raise TypeError
        self._this = collis.Line(*points[0], *points[1])
        self._data = self._this.get_data()
        self._v = self._this.get_v()

    def dot(self, line_obj) -> float:
        if(not isinstance(line_obj, Line)):
            raise TypeError
        temp = collis.Line(*line_obj.data)
        return self._this.dot(temp)

    def angle_btw_line(self, line_obj) -> float:
        if(not isinstance(line_obj, Line)):
            raise TypeError
        temp = collis.Line(*line_obj.data)
        result = self._this.angle_btw_line(temp)
        del temp
        return result

    def find_slope(self) -> float:
        return self._this.find_slope()

    def find_equation(self) -> tuple:
        data = self._this.find_Eq_Line()
        return (data.c1, data.c2, data.c3)

    def print(self):
        return self._this.print_out()

    def length(self):
        return self._this.length()

    def midpoint(self, point=True):
        p = self._this.midpoint()
        data = (p.x, p.y)
        del p
        if(point):
            return Point(data)

        else:
            return data

    def distance_point2line(self, point) -> float:
        if(isinstance(point, Point)):
            return self._this.distance_point2line(point.this)
        elif(isinstance(point, list) or isinstance(point, tuple)):
            if(len(point) != 2):
                raise TypeError
            return self._this.distance_point2line(collis.Point(*point))
        else:
            raise TypeError

    @property
    def data(self):
        return self._data

    def __del__(self):
        del self._this
        del self._data


class Point:
    def __init__(self, data: list) -> None:
        if(len(data) != 2):
            raise TypeError
        self._this = collis.Point(*data)
        self._data = (self._this.x, self._this.y)

    @property
    def this(self):
        return self._this

    @property
    def data(self):
        return self._data

    def __sub__(self, other) -> Line:
        p1_data = self.data
        p2_data = other.data
        return Line([p1_data, p2_data])

    def __str__(self) -> str:
        return f"{self._data}"

    def __del__(self):
        del self._this
        del self._data


class Circle:
    def __init__(self, para: list) -> None:
        '''
        [0]=r [1:]=center
        '''
        if(len(para) != 3):
            raise TypeError
        self._this = collis.Circle(*para)
        self._data = self._this.get_data()

    def print(self):
        self._this.print_out()

    def point_inside_range(self, point) -> bool:
        if(isinstance(point, Point)):
            if(self._this.point_inside_range(*point.data)):
                return True
            else:
                return False

        elif(isinstance(point, list)):
            if(len(point) != 2):
                raise TypeError
            if(self._this.point_inside_range(*point)):
                return True
            else:
                return False
        else:
            raise TypeError

    def project_to_circle(self, point, return_Point=False):
        if(isinstance(point, Point)):
            temp = self._this.point_inside_range(*point.data)

            if(return_Point):
                return Point([temp.x, temp.y])
            else:
                return (temp.x, temp.y)

        elif(isinstance(point, list) or isinstance(point, tuple)):
            if(len(point) != 2):
                raise TypeError
            temp = self._this.project_to_circle(*point)

            if(return_Point):
                return Point([temp.x, temp.y])
            else:
                return (temp.x, temp.y)
        else:
            raise TypeError

    def in_region(self, circle_obj) -> bool:
        result = self._this.in_region(circle_obj.this)
        return result

    @property
    def this(self):
        return self._this

    def __del__(self):
        del self._this
        del self._data


if __name__ == "__main__":
    l1 = Line([[0, 0], [6, 3]])
    l2 = Line([[0, 0], [-3, 6.001]])
    print(l1.find_equation())
    cc = Circle([2, 4.5375908692821, 4.67620525479])
    pp = cc.project_to_circle([4.2246769300936, 7.7543349047401])
    jj = Circle([2, 100.4375908692821, 4.67620525479])
    print(cc.in_region(jj))

    print(pp)
    hi = "hello world"
    print(hi[-3:-1])
