# Joon Lim 109558002
# hw4.py
# 6x6 Sudoku Solver

# To simplify our loop, we are going to represent the puzzle as an array of
# size 36 rather than a 6x6 2D array.
#
# Each row, column, and box will be assigned an index.
#
# The puzzle's indices will look like this:
#
#      0    1    2    3    4    5
#    +----+----+----+----+----+----+
#  0 | 0  | 1  | 2  | 3  | 4  | 5  |
#    +----+----+----+----+----+----+
#  1 | 6  | 7  | 8  | 9  | 10 | 11 |
#    +----+----+----+----+----+----+
#  2 | 12 | 13 | 14 | 15 | 16 | 17 |
#    +----+----+----+----+----+----+
#  3 | 18 | 19 | 20 | 21 | 22 | 23 |
#    +----+----+----+----+----+----+
#  4 | 24 | 25 | 26 | 27 | 28 | 29 |
#    +----+----+----+----+----+----+
#  5 | 30 | 31 | 32 | 33 | 34 | 35 |
#    +----+----+----+----+----+----+
#
# The boxes are like this:
#
#    +----+----+----+----+----+----+
#    |              |              |
#    |      0       |      1       |
#    |              |              |
#    +----+----+----+----+----+----+
#    |              |              |
#    |      2       |      3       |
#    |              |              |
#    +----+----+----+----+----+----+
#    |              |              |
#    |      4       |      5       |
#    |              |              |
#    +----+----+----+----+----+----+
#
# Thus, each square object can be identified by a unique trio of row, column,
# and box.
# Ex: square UA1 is square 0.


class Square(object):

    def __init__(self, row, col, box, name):
        self.value = 0  # initial value set to 0.
        self.possibilities = set()  # set of possibilities
        self.num_possibilities = 0

        self.row = row
        self.col = col
        self.box = box

        self.name = name

    # Use to see if we can add a value to the Square's list of possibilities
    def can_set(self, value):
        if self.row.contains(value) or \
           self.col.contains(value) or \
           self.box.contains(value):

            return False
        return True

    # Add value to set of possibilities and increase num_possibilities by 1
    def add_posible(self, value):
        assert value not in self.possibilities

        self.possibilities.add(value)
        self.num_possibilities += 1

    # Reset the set of possibilities and set num_possibilities to 0
    def reset_possibilities(self):
        self.possibilities.clear()
        self.num_possibilities = 0

    # set the value to given value and update all this Square's rows, columns,
    # and boxes
    def set_value(self, value):
        assert self.value is 0
        # print("Adding: ", value, "to", self.name)
        if value is not 0:
            self.value = value
            self.row.add(value)
            self.col.add(value)
            self.box.add(value)

# We only need one Zone class to represent the class of Row, Column, and
# box


class Zone(object):

    def __init__(self):
        self.values = set()

    def contains(self, value):
        contains = value in self.values
        # if contains is False:
        #     print(self.values)
        return contains

    # Should only be called whenever a new value is set to a square
    def add(self, value):
        assert value not in self.values or value is 0
        self.values.add(value)
        # print(self.values)


class Puzzle(object):

    def __init__(self, file_contents):
        self.rows = []
        self.cols = []
        self.boxes = []
        self.squares = []

        # Construct all rows, cols, and boxes
        for i in range(6):
            self.rows.append(Zone())
            self.cols.append(Zone())
            self.boxes.append(Zone())

        # Construct 36 Squares
        # This is order in which we need to set rows, cols, and boxes
        # Assuming the order is Row/Column/box:
        #
        #    +----+----+----+----+----+----+
        #    | 000| 010| 020| 031| 041| 051|
        #    +----+----+----+----+----+----+
        #    | 100| 110| 120| 131| 141| 151|
        #    +----+----+----+----+----+----+
        #    | 202| 212| 222| 233| 243| 253|
        #    +----+----+----+----+----+----+
        #    | 302| 312| 322| 333| 343| 353|
        #    +----+----+----+----+----+----+
        #    | 404| 414| 424| 435| 445| 455|
        #    +----+----+----+----+----+----+
        #    | 504| 514| 524| 535| 545| 555|
        #    +----+----+----+----+----+----+
        # box number is tricky
        # The simplest way is with a string

        box_nums = "000111000111222333222333444555444555"
        for i in range(36):
            row_num = i // 6
            col_num = i % 6
            box_num = int(box_nums[i])
            name = str(row_num) + str(col_num) + str(box_num)
            self.squares.append(Square(self.rows[row_num],
                                       self.cols[col_num],
                                       self.boxes[box_num],
                                       name))
            # set the value in square, which will update its row, col, and box
            if file_contents[i] is "-":
                self.squares[i].set_value(0)
            else:
                self.squares[i].set_value(int(file_contents[i]))

    # print the puzzle to stdout
    def print_puzzle(self):
        for i in range(0, 36, 6):
            value1 = str(self.squares[i].value)
            value2 = str(self.squares[i + 1].value)
            value3 = str(self.squares[i + 2].value)
            value4 = str(self.squares[i + 3].value)
            value5 = str(self.squares[i + 4].value)
            value6 = str(self.squares[i + 5].value)
            print(value1, value2, value3, value4, value5, value6)

import sys
# import time


def main():

    # file containing 36 whitespace-separated entries
    input_file = open(sys.argv[1], "r")
    file_contents = input_file.read()
    file_contents = file_contents.split()

    puzzle = Puzzle(file_contents)
    # puzzle.print_puzzle()

    iterations = 0  # number of times we checked the whole puzzle
    puzzle_was_updated = True

    # print("\nStart\n")

    # time_start = time.time()

    while(True):
        if puzzle_was_updated is False:
            # done!
            # TODO: for harder puzzles, this algorithm will not work.
            # Implement a way to detect if a puzzle is finished or not.
            # If not finished, we must use brute force to solve the
            # remaining spots: try all possible combinations until we fine
            # one that works.
            break

        puzzle_was_updated = False

        for square in puzzle.squares:
            # only care about squares we haven't solved
            if (square.value is 0):
                # relinquish list of possibilities and
                # set num_possibilities to 0
                square.reset_possibilities()

                for x in range(1, 7):
                    if square.can_set(x):
                        square.add_posible(x)
                    else:
                        continue

                if square.num_possibilities is 1:
                    # only 1 possibility. this must go in the square!
                    # every time we update a value of the square,
                    # the value of the square in each pertaining row, col,
                    # and box will update as well
                    square.set_value(square.possibilities.pop())
                    puzzle_was_updated = True

        iterations += 1

    # time_end = time.time()
    # print(str(time_end - time_start), "\n")

    # print(str(iterations), "iterations\n")
    puzzle.print_puzzle()

main()
