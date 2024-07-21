#################################################################
# FILE : board.py
# WRITER : yotam megged , yotam267 , 319134912
# EXERCISE : intro2cs ex9 2022C
# DESCRIPTION: A class of board that can add objects of class car and move them
# WEB PAGES I USED: stack over flow, programiz
#################################################################
BOARD_SIZE = 7
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


class Board:
    """
    an object of Board will have dictionary of all it's coordinates and their values. a coordinate's value will be
    None unless there's a Car object in it, then it will get the value of the name of the car.
    the board will also have a dictionary of all the cars which are on the board, and will support methods that move
    a car, print the board and more
    """
    def __init__(self):
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        board = {}
        # will look like: {(0,0): "Y"} if the car named "Y" sits is the (0,0) location
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                board.update({(row, col): None})
                if (row, col) == (3, 6):
                    board.update({(3, 7): None})
        self.__board = board
        self.__cars = {}
        # will look like: {"Y": car1} if car1 is a Car object and its name is "Y"


    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        #The game may assume this function returns a reasonable representation
        #of the board for printing, but may not assume details about it.
        board_string = ""
        for coordinate in self.__board:
            if not self.__board[coordinate]:
                # if the current coordinate is empty
                if coordinate == (3,7):
                    # the target coord
                    board_string += "E"
                else:
                    board_string += "_"
            else:
                # we add the car name
                board_string += str(self.__board[coordinate])
            if coordinate == (3, 6):
                # then we don't want to go down a line
                board_string += " "
            elif coordinate == (3, 7):
                board_string += "\n"
            elif coordinate[1] != 6:
                board_string += " "
            else:
                # we reached the end of the current line of the board
                board_string += "\n"
        return board_string

    def check_coords_validity(self, location_list):
        """
        checks if all the locations is a list are valid: are inside the board and not occupied by another car
        :param location_list: a list of coordinates
        :return: true if all the coordinates are inside the board and not occupied, false otherwise
        """
        for location in location_list:
            if location not in self.cell_list():
                return False
            elif self.__board[location]:
                return False
        return True

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        #In this board, returns a list containing the cells in the square
        #from (0,0) to (6,6) and the target cell (3,7)
        cell_list = list(self.__board.keys())
        return cell_list

    def is_move_allowed(self, car, movekey):
        """
        checks if a move is allowed based on a car and a movekey, assuming the car is on the board and the movekey
         is legal - if the location the car "wants" to go to, is inside the board and not occupied
        :param car: an instance of class car
        :param movekey: a movekey
        :return:
        """
        move_target_list = car.movement_requirements(movekey)
        for move_target in move_target_list:
            if move_target not in self.cell_list() or self.__board[move_target]:
                return False
        return True


    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        #From the provided example car_config.json file, the return value could be
        #[('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        possible_car_moves = []
        for car_name in self.__cars:
            car = self.__cars[car_name]
            moves_dic = car.possible_moves()
            for move in moves_dic:
                if self.is_move_allowed(car, move):
                    # we only need moves that are allowed on the board
                    move_tuple = (car_name, move, moves_dic[move])
                    possible_car_moves.append(move_tuple)
        return possible_car_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        #In this board, returns (3,7)
        return 3, 7

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        # implement your code and erase the "pass"
        return self.__board[coordinate]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        #Remember to consider all the reasons adding a car can fail.
        #You may assume the car is a legal car object following the API.
        if car.get_name() in self.__cars:
            # cannot add a car that is already on the board
            return False
        elif not self.check_coords_validity(car.car_coordinates()):
            # cannot add a car if collides with another car or sits outside the board
            return False
        else:
            car_locations = car.car_coordinates()
            for location in car_locations:
                self.__board[location] = car.get_name()
                # update the board
            self.__cars.update({car.get_name(): car})
            # update the cars dictionary
            return True

    def update_car_move(self, car_name, movekey):
        """
        given valid car name and movkey, and assuming the car can move based on the board situation, this function
        moves the car and updates the board by removing the car's name from the board then adding it after it has moved
        (this may not be the most efficient way, but it is the simplest)
        :param car_name: a name of a car which is on the board
        :param movekey: a valid movekey that the car can go to based on the board situation
        :return:
        """
        for location in self.__cars[car_name].car_coordinates():
            self.__board[location] = None
        self.__cars[car_name].move(movekey)
        for coord in self.__cars[car_name].car_coordinates():
            self.__board[coord] = car_name

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        if name not in self.__cars:
            # there's no such car on the board
            print("car not on the board")
            return False
        elif not self.__cars[name].movement_requirements(movekey):
            # if the movekey doesn't match the car's orientation
            print("invalid movekey")
            return False
        elif not self.is_move_allowed(self.__cars[name], movekey):
            # if the movekey is fine but the location the car wants to go to is occupied
            # or outside the board
            print("this move is not allowed")
            return False
        else:
            self.update_car_move(name, movekey)
            return True


