import random as rd
import math
import time


def distance(d1: tuple, d2: tuple):
    """
    finding the distance between two points
    :param d1: first dot
    :param d2: second dot
    :return: distance
    """
    x1, y1 = d1
    x2, y2 = d2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def getRegionShape():
    """
    selects the bot action Region
    """
    r = Region("""get your image here""")
    return r.x, r.y, r.w, r.h, r


class Window:
    """ class implementing the window (emulator) """
    def __init__(self, dot: tuple, h: int, w: int):
        """
        constructor
        :param dot: top left window
        :param h: window height
        :param w: window width
        """
        self.dot = dot
        self.h = h
        self.w = w
        self.center = (dot[0] + int(w/2), dot[1] + int(h/2))

        # angle between window diagonal and x axis
        self.angle = math.atan((self.dot[0] + self.w) / (self.dot[1] + self.h))

    def shape(self):
        """
        :return: the four point tuple (defining window)
        """
        return self.dot, (self.dot[0] + self.w, self.dot[1]), (self.dot[0] + self.w, self.dot[1] + self.h),\
               (self.dot[0], self.dot[1] + self.h)


class Runner:
    """ character class """
    def __init__(self, window: Window):
        """
        constructor
        :param window: emulator window
        """
        self.start = (0, 0)
        self.current = (0, 0)
        self.window = window

    def go(self, location: tuple):
        """
        character move
        :param location: destination coordinates
        :return: None
        """
        x, y = location  # in absolute display coordinates
        # in emulator window coordinates
        tmp_x = x - self.window.dot[0]
        tmp_y = y - self.window.dot[1]

        # in character coordinates
        new_x = tmp_x - self.window.center[0]
        new_y = tmp_y - self.window.center[1]

        self.current = (new_x, new_y)
        click(Location(*location))

    def _get_random_angle(self, deviation=5):
        """
        :param deviation: deviation
        :return: random angle
        """
        ...

    def _get_random_length(self):
        """
        :return: random length
        """
        diagonal = math.sqrt((self.window.dot[0] + self.window.w)**2 + (self.window.dot[1] + self.window.h)**2)
        max_len = int(diagonal / 2)
        return rd.randrange(5, max_len - 10)

    def anotherWay(self):
        """
        alternate move
        used when there are no items or character in a dead end
        :return: None
        """
        z = Runner._get_random_length()  # diagonal
        len_x = z * math.cos(self.window.angle)
        len_y = z * math.sin(self.window.angle)
        new_x = abs(self.current[0] - len_x)
        new_y = abs(self.current[1] - len_y)

        # in emulator window
        x_for_click = new_x - self.window.center[0]
        y_for_click = new_y - self.window.center[1]

        # in absolute coordinates
        x_for_click -= self.window.dot[0]
        y_for_click -= self.window.dot[1]

        self.go((x_for_click, y_for_click))

