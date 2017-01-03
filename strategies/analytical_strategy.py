import random

from engine.warships import GridPoint, Grid, CheckResult
from strategies.strategy import Strategy


class AnalyticalStrategy(Strategy):
    def run(self, grid: Grid):
        self.init_vars(grid)

        while not grid.is_won():
            if self.mode == "HUNT":
                self.hunt()
            elif self.mode == "DESTROY":
                self.destroy()
                self.mode = "HUNT"

    def init_vars(self, grid: Grid):
        self.mode = "HUNT"  # or "DESTROY", respectively
        self.dont_check = []
        self.first_ship_point = None
        self.grid = grid
        self.alive_ships = {i.length: i.quantity for i in grid.ship_config}

    def destroy(self):
        ship_points = [self.first_ship_point]

        possible_points = self.list_of_eligible_points(ship_points)
        next_point = self.find_next_ship_point(possible_points, ship_points)  # TODO: this must depend on probability!

        if next_point is None:  # = we found ship of length 2
            self.update_dont_check_points(ship_points)
            return

        ship_points.append(next_point)
        direction_of_ship = self.find_direction_of_ship(ship_points)
        self.find_rest_of_ship(direction_of_ship, ship_points)
        self.update_dont_check_points(ship_points)

    def list_of_eligible_points(self, ship_points):
        points_list = []
        point = ship_points[0]
        for i in GridPoint.directions:
            try:
                points_list.append(point.move(i))
            except ValueError:
                pass
        return points_list

    def find_next_ship_point(self, possible_points, ship_points):
        while True:  # repeat until you hit ship cell
            random_point = random.choice(possible_points)
            possible_points.remove(random_point)
            result = self.do_check(random_point)
            if "MISS" in result:
                pass
            elif "HIT" in result:
                return random_point
            elif "SUNK" in result:
                self.mark_sunk(result.length)
                ship_points.append(random_point)
                return None  # None means that we found all ship cells

    def find_direction_of_ship(self, ship_points):
        first_point = ship_points[0]
        second_point = ship_points[1]

        if first_point.x == second_point.x - 1 or first_point.x - 1 == second_point.x:  # on what line ship is:
            return ["left", "right"]  # horizontal, or...
        else:
            return ["down", "up"]  # vertical

    def find_rest_of_ship(self, directions, ship_points):
        for i in range(2):
            is_ship_cell = True
            direction = random.choice(directions)
            directions.remove(direction)

            if ship_points[0].is_on(direction, ship_points[1]):
                point = ship_points[0]
            else:
                point = ship_points[1]

            while is_ship_cell:  # repeat until we hit non-ship cell
                try:
                    point = point.move(direction)
                    result = self.do_check(point)
                    if "MISS" in result:
                        # that means we are returning to the starting point and trying again in other direction
                        is_ship_cell = False
                    elif "HIT" in result:
                        is_ship_cell = True
                        ship_points.append(point)
                    elif "SUNK" in result:
                        ship_points.append(point)
                        self.mark_sunk(result.length)
                        return
                except ValueError:
                    break

    def hunt(self):
        point = self.pick_most_probable_hunt_point()
        result_of_check = self.do_check(point)
        if "MISS" in result_of_check:
            self.mode = "HUNT"
        elif "HIT" in result_of_check:
            self.mode = "DESTROY"
            self.first_ship_point = point
        elif "SUNK" in result_of_check:
            self.update_dont_check_points([point])
            self.mode = "HUNT"
            self.mark_sunk(result_of_check.length)

    def pick_most_probable_hunt_point(self):

        probability_grid = [[0 for x in range(10)] for y in range(10)]

        def test(direction, length, x, y):
            try:
                GridPoint(x, y).move(direction, times=length - 1)
            except ValueError:
                return
            for delta in range(length):
                point_to_check = GridPoint(x, y).move(direction, times=delta)
                if self.grid.is_checked(point_to_check) or point_to_check in self.dont_check:
                    return False  # that position is not available
            for delta in range(length):  # if that position is available:
                point_to_add = GridPoint(x, y).move(direction, times=delta)
                probability_grid[point_to_add.y][point_to_add.x] += length - delta
                return True

        def reduce_probability_grid():
            max = [0, 0]
            for x in range(10):
                for y in range(10):
                    if probability_grid[y][x] > probability_grid[max[0]][max[1]]:
                        max = [y, x]
            return GridPoint(max[1], max[0])

        for x in range(10):
            for y in range(10):
                for direction in GridPoint.directions:
                    for length in reversed(sorted(self.alive_ships)):
                        if self.alive_ships[length] != 0:
                            if test(direction, length, x, y):
                                break

        return reduce_probability_grid()

    def update_dont_check_points(self, points_to_check_around):
        offsets = [-1, 0, 1]
        for i in points_to_check_around:
            for x in offsets:
                for y in offsets:
                    try:
                        point = GridPoint(i.x + x, i.y + y)
                        if not self.grid.is_checked(point) and point not in self.dont_check:
                            self.dont_check.append(point)
                            self.grid.mark(point, "*")
                            # print(self.grid)
                    except:
                        pass

    def do_check(self, point: GridPoint) -> CheckResult:
        if (not self.grid.is_checked(point)) and (point not in self.dont_check):
            check_result = self.grid.check(point)
            # print(self.grid)
            return check_result
        return CheckResult("MISS")

    def mark_sunk(self, length):
        self.alive_ships[length] -= 1
