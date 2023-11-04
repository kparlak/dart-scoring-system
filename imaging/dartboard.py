import numpy as np
import math

class Dartboard:
    def __init__(self) -> None:
        self.x0 = 0.0
        self.y0 = 0.0
        self.factor = 25.4/60 # mm/pixel (60 pixels/inch from center - 25.4 mm)
        self.radius = 0.0
        self.theta = 0.0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.dist_x = 0.0
        self.dist_y = 0.0
        self.calibrate()

    def get_center(self):
        return self.x0, self.y0

    def get_radius(self):
        return self.radius

    def get_theta(self):
        return self.theta

    def get_pos(self):
        return self.pos_x, self.pos_y

    def get_dist(self):
        return self.dist_x, self.dist_y

    def calibrate(self):
        self.H = [[1.00243107e+00, 2.98250358e-01,-2.62532023e+02],
                  [1.29748450e-07, 1.72156056e+00, 1.88249310e+02],
                  [2.14034568e-10, 6.54323960e-04, 1.00000000e+00]]
        # self.H = np.genfromtxt("H.txt", delimiter=",", dtype=float)

    def translate_pos(self, x, y):
        point = np.array([x, y, 1])
        new_point = np.dot(self.H, point)
        new_point = new_point / new_point[2]
        return new_point

    def set_center(self, x, y):
        # Translate position
        center = self.translate_pos(x, y)
        self.x0 = x * self.factor
        self.y0 = center[1] * self.factor

    def calc_radius(self, x, y):
        return math.sqrt(math.pow(x, 2) + math.pow(y, 2))

    def map_ring(self, radius):
        if radius >= 162 and radius < 170:
            return 'A'
        elif radius >= 107 and radius < 162:
            return 'B'
        elif radius >= 99 and radius < 107:
            return 'C'
        elif radius >= 16 and radius < 99:
            return 'D'
        elif radius >= 6.35 and radius < 16:
            return 'X'
        elif radius >= 0 and radius < 6.35:
            return 'Y'
        else:
            return 'Z'

    def update_ring(self, x, y):
        self.radius = self.calc_radius(x, y)
        return self.map_ring(radius=self.radius)

    def calc_theta(self, x, y):
        # Compute quadrant for calculation
        if x > 0.0 and y > 0.0: # Quadrant 1
            theta = math.atan(abs(y) / abs(x))
        elif x < 0.0 and y > 0.0: # Quadrant 2
            theta = math.atan(abs(x) / abs(y)) + (math.pi / 2)
        elif x < 0.0 and y < 0.0: # Quadrant 3
            theta = math.atan(abs(y) / abs(x)) + math.pi
        elif x > 0.0 and y < 0.0: # Quadrant 4
            theta = math.atan(abs(x) / abs(y)) + (3 * math.pi / 2)
        else:
            theta = 0.0
        # Convert to degrees
        return math.degrees(theta)

    def map_number(self, theta):
        if (theta >= 351 and theta <= 360) or (theta >= 0 and theta < 9):
            return 20
        elif theta >= 9 and theta < 27:
            return 5
        elif theta >= 27 and theta < 45:
            return 12
        elif theta >= 45 and theta < 63:
            return 9
        elif theta >= 63 and theta < 81:
            return 14
        elif theta >= 81 and theta < 99:
            return 11
        elif theta >= 99 and theta < 117:
            return 8
        elif theta >= 117 and theta < 135:
            return 16
        elif theta >= 135 and theta < 153:
            return 7
        elif theta >= 153 and theta < 171:
            return 19
        elif theta >= 171 and theta < 189:
            return 3
        elif theta >= 189 and theta < 207:
            return 17
        elif theta >= 207 and theta < 225:
            return 2
        elif theta >= 225 and theta < 243:
            return 15
        elif theta >= 243 and theta < 261:
            return 10
        elif theta >= 261 and theta < 279:
            return 6
        elif theta >= 279 and theta < 297:
            return 13
        elif theta >= 297 and theta < 315:
            return 4
        elif theta >= 315 and theta < 333:
            return 18
        elif theta >= 333 and theta < 351:
            return 1
        else:
            return 0

    def update_number(self, x, y):
        self.theta = self.calc_theta(x, y)
        return self.map_number(self.theta)

    def update(self, x, y):
        # Translate position
        pos = self.translate_pos(x, y)
        self.pos_x = x * self.factor
        self.pos_y = pos[1] * self.factor
        # Calculate distance from center
        self.dist_x = self.pos_x - self.x0
        self.dist_y = self.y0 - self.pos_y
        return self.update_number(self.dist_x, self.dist_y), self.update_ring(self.dist_x, self.dist_y)

# EOF
