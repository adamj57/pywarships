import random
from typing import Iterable, List


class CheckResult:

    def __init__(self, state, length=0):
        self.state = state
        self.length = length

    def __contains__(self, item):
        return self.state == item

    def __str__(self):
        if self.state == "SUNK":
            return "{}, {}".format(self.state, self.length)
        else:
            return self.state


class GridPoint:
    directions = ["left", "right", "up", "down"]

    def __init__(self, x, y):
        if x < 0 or x > 9:
            raise ValueError("X must be in range 0-9!")
        if y < 0 or y > 9:
            raise ValueError("Y must be in range 0-9!")
        self.x, self.y = x, y

    def move(self, direction: str, times=1):
        direction = direction.lower()
        x_delta = 0
        y_delta = 0
        for i in range(times):
            if direction == "left":
                x_delta -= 1
            elif direction == "right":
                x_delta += 1
            elif direction == "up":
                y_delta -= 1
            elif direction == "down":
                y_delta += 1
            else:
                raise ValueError("Direction must be 'up', 'down', 'left' or 'right'!")
        return GridPoint(self.x + x_delta, self.y + y_delta)

    def is_on(self, direction, other):
        try:
            ret = other.move(direction) == self
        except ValueError:
            return False
        return ret

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __str__(self):
        return "x: {} y: {}".format(self.x, self.y)


class Cell:
    def __init__(self, point: GridPoint):
        self.__is_ship_cell = False
        self.__checked = False
        self.position = point
        self.__custom_marker = None

    def checked(self, *args):
        if len(args) == 0:
            return self.__checked
        elif args[0]:
            self.__checked = True

    def ship_cell(self, *args):
        if len(args) == 0:
            return self.__is_ship_cell
        elif args[0]:
            self.__is_ship_cell = True

    def set_marker(self, marker):
        self.__custom_marker = marker

    def __str__(self):
        if self.__custom_marker is None:
            if self.ship_cell():
                if self.checked():
                    return "V"
                else:
                    return "O"
            else:
                if self.checked():
                    return "X"
                else:
                    return "."
        else:
            return self.__custom_marker

    def __eq__(self, other):
        return self.ship_cell() == other.ship_cell and self.checked() == other.checked()


class SunkError(Exception):
    pass


class Ship:

    def __init__(self, cells: List[Cell]):
        self.cells = cells

    def has_point(self, point_to_find: GridPoint):
        for cell in self.cells:
            if cell.position == point_to_find:
                return True
        return False

    def hit(self, point: GridPoint):
        if self.is_sunk():
            raise SunkError("This ship is already sunk!")
        for cell in self.cells:
            if cell.position == point:
                cell.checked(True)
                return
        raise ValueError("Point of coordinates x: {} and y: {} is not in this ship!".format(point.x, point.y))

    def is_sunk(self):
        for cell in self.cells:
            if not cell.checked():
                return False
        return True

    def __len__(self):
        return len(self.cells)


class Grid:
    def __init__(self):
        self.__grid = self.generate_blank_grid()
        self.checked_cells = 0
        self.__checked_ship_cells = 0
        self.__ships = []
        self.ship_config = ShipConfig()

    def generate_blank_grid(self):
        return [[Cell(GridPoint(x, y)) for x in range(10)] for y in range(10)]

    def place_ship(self, point, direction, length):
        valid_coords = []
        for i in range(length):
            self.__check_ship_nearby(point)
            valid_coords.append(point)
            point = point.move(direction)
        for point in valid_coords:
            self.__cell_at(point).ship_cell(True)
        ship = Ship([self.__cell_at(point) for point in valid_coords])
        self.__ships.append(ship)
        self.ship_config.add_ship_of_length(length)

    def __check_ship_nearby(self, point):
        def check_offset(point, x_offset, y_offset):
            if point.x + x_offset < 0 or point.x + x_offset > 9:
                return
            if point.y + y_offset < 0 or point.y + y_offset > 9:
                return
            if self.__cell_at(GridPoint(point.x + x_offset, point.y + y_offset)).ship_cell():
                raise ValueError("You can't place ship here!")

        offsets = [-1, 0, 1]
        for x in offsets:
            for y in offsets:
                check_offset(point, x, y)

    def __cell_at(self, point):
        return self.__grid[point.y][point.x]

    def check(self, point: GridPoint) -> CheckResult:
        if self.__cell_at(point).ship_cell():
            self.__checked_ship_cells += 1
            for i in self.__ships:
                if i.has_point(point):
                    i.hit(point)
                    if i.is_sunk():
                        ret = CheckResult("SUNK", len(i))
                    else:
                        ret = CheckResult("HIT")
        else:
            ret = CheckResult("MISS")
        self.__cell_at(point).checked(True)
        self.checked_cells += 1
        return ret

    def is_checked(self, point):
        return self.__cell_at(point).checked()

    def is_won(self):
        for ship in self.__ships:
            if not ship.is_sunk():
                return False
        return True

    def mark(self, point: GridPoint, marker: str):
        self.__cell_at(point).set_marker(marker)

    def __str__(self):
        string = "  0 1 2 3 4 5 6 7 8 9\n"
        for i, row in enumerate(self.__grid):
            string += str(i)
            string += " "
            for item in row:
                string += str(item) + " "
            string += "\n"
        return string


class ShipConfig:

    class ShipDetails:

        def __init__(self, length, quantity):
            self.length = length
            self.quantity = quantity

    def __init__(self, config=None):
        self.predefined = {"polish": [self.ShipDetails(4, 1), self.ShipDetails(3, 2),
                                      self.ShipDetails(2, 3), self.ShipDetails(1, 4)]}

        if not (config is None):
            try:
                self.config = self.predefined[config]
            except KeyError:
                raise ValueError("Config of name {} does not exist!".format(config))
        else:
            self.config = []

    def add_ship_details(self, length, quantity):
        self.config.append(self.ShipDetails(length, quantity))

    def add_ship_of_length(self, length):
        for i in self.config:
            if i.length == length:
                i.quantity += 1
                return
        self.config.append(self.ShipDetails(length, 1))

    def __iter__(self):
        self.index = 0
        self.config.sort(key=lambda ship_detail: ship_detail.length, reverse=True)
        return self

    def __next__(self):
        try:
            ret = self.config[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return ret


def gen_rand_grid(config: ShipConfig):
    grid = Grid()

    def place_random_ship(size):  # TODO: embed mechanizm that checks if ship can be placed or not
        ship_placed = False
        tries_count = 0
        while not ship_placed and tries_count < 50:
            point = GridPoint(random.randint(0, 9), random.randint(0, 9))
            direction = random.choice(GridPoint.directions)
            try:
                grid.place_ship(point, direction, size)
                ship_placed = True
            except ValueError:
                pass
            tries_count += 1

        return ship_placed

    for ship_detail in config:
        for i in range(ship_detail.quantity):
            place_random_ship(ship_detail.length)

    return grid
