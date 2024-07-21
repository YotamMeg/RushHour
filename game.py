#################################################################
# FILE : game.py
# WRITER : yotam megged , yotam267 , 319134912
# EXERCISE : intro2cs ex9 2022C
# DESCRIPTION: A class of game, contains a board. then adds cars to it from a json file, and asks the user
# to move cars around until he wins or chooses to stop
# WEB PAGES I USED: stack over flow, programiz
#################################################################

import board
from car import *
import helper
import sys

CAR_NAMES = "YBOWGR"
MAX_CAR_LENGTH = 4
MIN_CAR_LENGTH = 2
CAR_DIRECTIONS = "udlr"
PLAYER_DONE = "!"
PLAY_TURN_STR = "Choose a car to move and a direction, or type '!' to finish the game: "
INVALID_INPUT = "Invalid input! please pick a legal car name and direction "
CAR_CANNOT_MOVE = "The car you picked cannot move in this direction! please choose a different car or direction "
WIN_MESSAGE = "Congrats! you have won!"
STOP_MESSAGE = "Too bad, this game is the best, try again when you grow a pair"
VERTICAL = 0
HORIZONTAL = 1
ORIENTATIONS = {VERTICAL, HORIZONTAL}


class Game:
    """
    a game object has an object of class Board.
    it runs a game by adding to the board cars that are legal based on the given requirements, then asks for input
    from the user, if it's not valid, it asks for a new one, and if it is, it moves a car on the board. it does so
    until the player wants to stop or wins
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        self.__board = board

    def is_input_valid(self, user_input):
        """
        checks if the input is valid based on the given requirements - only 'car_name,car_direction'
        is a legal input, and only if the car name and direction are within the legal names that were given.
        notice that an input - '!' will be illegal based on this function, but we will check it during the game
        :param user_input: the user input
        :return: true if the input is valid, false if not
        """
        if len(user_input) != 3 or user_input[0] not in CAR_NAMES or user_input[1] != "," or \
                user_input[2] not in CAR_DIRECTIONS:
            return False
        return True

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        # implement your code here (and then delete the next line - 'pass')

        user_input = input(PLAY_TURN_STR)
        if user_input == "!":
            # then we need to exit the game without trying to move a car
            return True
        while not self.is_input_valid(user_input) or not self.__board.move_car(user_input[0], user_input[2]):
            # if the input is valid, we try to move a car based on the input (and we will get the value true and
            # not enter the while loop). if we couldn't move a car (got a false value) or the input was illegal we
            # will enter the loop, print an appropriate message and recheck the new input. the turn will end only
            # when the user successfully moved a car, then we will return false, or when the user wishes to stop
            if user_input == "!":
                return True
            if not self.is_input_valid(user_input):
                user_input = input(INVALID_INPUT)
            else:
                user_input = input(CAR_CANNOT_MOVE)
        # we print the current status of the board after every successful turn
        print(self.__board)
        return False

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        calls the single turn function over and over, until it returns a value - true, meaning the player wants
        to stop playing, or when a car has reached the target location, meaning the player has won
        :return: None
        """
        target_location = self.__board.target_location()
        game_over = False
        print(self.__board)
        while not game_over and not self.__board.cell_content(target_location):
            # game over will get the value of single_turn, which will be true only
            # if the player wishes to stop
            # the other condition will be true only when a car is in the target location, in this case
            # the player has won
            game_over = self.__single_turn()
        if self.__board.cell_content(target_location):
            print(WIN_MESSAGE)
        else:
            print(STOP_MESSAGE)


if __name__ == "__main__":
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    def get_car_locations(car_specs):
        """
        receives car specs (length, location and orientation) and returns a list of all the locations the car is in
        :param car_specs: a list of car parameters
        :return: a list of locations
        """
        car_length = car_specs[0]
        car_location = tuple(car_specs[1])
        car_orientation = car_specs[2]
        car_locations = []
        for i in range(car_length):
            if car_orientation == HORIZONTAL:
                car_locations.append((car_location[0], car_location[1] + i))
            elif car_orientation == VERTICAL:
                car_locations.append((car_location[0] + i, car_location[1]))
        return car_locations

    def is_car_allowed(board, car_name, car_specs):
        """
        receives a car's name and specs, and checks if it is allowed on the board: if the car parameters are valid
        and if the coordinates of the car are in the board and unoccupied.
        :param board: an instance of board class
        :param car_name: a car's name
        :param car_specs: a list of car specs
        :return: true if the car is allowed on the board, false if not
        """
        car_length = car_specs[0]
        car_orientation = car_specs[2]
        if MIN_CAR_LENGTH > car_length or MAX_CAR_LENGTH < car_length or car_orientation not in ORIENTATIONS \
                or car_name not in CAR_NAMES:
            # first we check all the specs are valid
            return False
        car_locations = get_car_locations(car_specs)
        for location in car_locations:
            # now we check the locations
            if location not in board.cell_list() or board.cell_content(location):
                return False
        return True


    new_board = board.Board()
    new_game = Game(new_board)
    max_car_dictionary = helper.load_json(sys.argv[1])
    for car in max_car_dictionary:
        car_specs = max_car_dictionary[car]
        if is_car_allowed(new_board, car, car_specs):
            # we add only legal cars to the board, there's no need to check if a car is already in the board
            # before adding it because a dictionary cannot hold the same key twice, and anyway it is being checked
            # in the add car method of the board
            new_car = Car(car, car_specs[0], tuple(car_specs[1]), car_specs[2])
            new_board.add_car(new_car)
    new_game.play()
