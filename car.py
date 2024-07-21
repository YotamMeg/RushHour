#################################################################
# FILE : car.py
# WRITER : yotam megged , yotam267 , 319134912
# EXERCISE : intro2cs ex9 2022C
# DESCRIPTION: A class of car, can move cars and do other things
# WEB PAGES I USED: stack over flow, programiz
#################################################################

VERTICAL = 0
HORIZONTAL = 1
UP = "u"
DOWN = "d"
LEFT = "l"
RIGHT = "r"
UP_STRING = "cause the car to move a step up"
DOWN_STRING = "cause the car to move a step down"
LEFT_STRING = "cause the car to move one step to the left"
RIGHT_STRING = "cause the car to move one step to the right"


class Car:
    """
    an object of class car will have attributes of name, length, location, orientation, as well as a list of
    all the coordinates he's at (car_coordinates) and a far_end attribute which is the car's location farthest from
    the (0,0) coordinate.
    it will also have get methods that returns the name, list of locations and methods that will return the possible
    moves of the object, that will move it, and that will return a list of coordinates that should be empty in order
    for it to move.
    """
    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.
        # implement your code and erase the "pass"
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation
        location_list = []
        for car_space in range(self.__length):
            if self.__orientation == HORIZONTAL:
                location_list.append((self.__location[0], (self.__location[1] + car_space)))
            else:
                location_list.append((self.__location[0] + car_space, self.__location[1]))
        self.__coordinates = location_list
        self.__far_end = self.__coordinates[-1]
        # far_end is the location farthest from 0,0

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        list_of_coords = []
        for coord in self.__coordinates:
            list_of_coords.append(coord)
        return list_of_coords

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        #For this car type, keys are from 'udrl'
        #The keys for vertical cars are 'u' and 'd'.
        #The keys for horizontal cars are 'l' and 'r'.
        #You may choose appropriate strings.
        #The dictionary returned should look something like this:
        #result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        #A car returning this dictionary supports the commands 'f','d','a'.
        result = dict()
        if self.__orientation == VERTICAL:
            result.update({UP: UP_STRING})
            result.update({DOWN: DOWN_STRING})
        elif self.__orientation == HORIZONTAL:
            result.update({LEFT: LEFT_STRING})
            result.update({RIGHT: RIGHT_STRING})
        return result

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        #For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        #be empty in order to move down (with a key 'd').
        if self.__orientation == VERTICAL:
            if movekey == UP:
                return [(self.__location[0] - 1, self.__location[1])]
            elif movekey == DOWN:
                return [(self.__far_end[0] + 1, self.__location[1])]
        elif self.__orientation == HORIZONTAL:
            if movekey == LEFT:
                return [(self.__location[0], self.__location[1] - 1)]
            elif movekey == RIGHT:
                return [(self.__location[0], self.__far_end[1] + 1)]

    def update_car(self, movekey):
        """
        updates the relevant car's attributes when given a valid movekey - updates the car's location list, location
        and far end based on the movekey
        :param movekey: a valid moovkey that matches the car's orientation
        :return: true after updating the car's attributes
        """
        for index, location in enumerate(self.__coordinates):
            if movekey == RIGHT:
                self.__coordinates[index] = location[0], location[1] + 1
            elif movekey == LEFT:
                self.__coordinates[index] = location[0], location[1] - 1
            elif movekey == DOWN:
                self.__coordinates[index] = location[0] + 1, location[1]
            elif movekey == UP:
                self.__coordinates[index] = location[0] - 1, location[1]
        self.__location = self.__coordinates[0]
        self.__far_end = self.__coordinates[-1]
        return True

    def is_move_legal(self, movekey):
        """
        checks if a movekey is legal based on the car's orientation
        :param movekey: a movekey
        :return: true if its legal and false if not
        """
        if self.__orientation == VERTICAL:
            return movekey in [UP, DOWN]
        elif self.__orientation == HORIZONTAL:
            return movekey in [LEFT, RIGHT]

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if not self.is_move_legal(movekey):
            return False
        return self.update_car(movekey)

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name

