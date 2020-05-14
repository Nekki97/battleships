from header import *
from ship_funcs import *

def bot_place():

    def try_ship(ship, orientation, column, row, board):

        def get_coords(ship, orientation, column, row):
            debug = False
            coords = []
            length = get_length(ship)
            if debug: print("Ship:", ship, "length:", length)
            if orientation == "horizontal":
                for k in range(length):
                    coords.append((column + k, row))
                    if debug: print("Coords.append", (column+k, row))
            elif orientation == "vertical":
                for k in range(length):
                    coords.append((column, row + k))
                    if debug: print("Coords.append", (column, row+k))
            return coords

        board_coords = []

        false_report = False
        if len(board) == 0:
            pass
        else:
            for placed_ship in board:
                ship_name, placed_orientation, placed_column, placed_row = placed_ship
                ship_coords = get_coords(ship_name, placed_orientation, placed_column, placed_row)
                for coords in ship_coords:
                    board_coords.append(coords)

                if debug: print("Board coords", board_coords)

        length = get_length(ship)

        if orientation == "horizontal":
            for k in range(length):
                if (column + k, row) in board_coords:
                    if false_report: print("False5")
                    return False
                elif column + k > 10:
                    if false_report: print("False6")
                    return False

        elif orientation == "vertical":
            for k in range(length):
                if (column, row + k) in board_coords:
                    if false_report: print("False7")
                    return False
                elif row + k > 10:
                    if false_report: print("False8")
                    return False

        return True

    debug = False
    board = []
    if debug: print("BOT IS PLACING")
    global seek_lock_0
    global ships

    ships_right = []
    for ship in ships:
        if "right" in ship:
            ships_right.append(ship)

    while len(ships_right) > 0:
        ship = random.choice(ships_right)
        orientation = random.choice(["horizontal", "vertical"])
        column = random.randint(1, 10)
        row = random.randint(1, 10)

        if orientation == "vertical":
            x, y = flip_ship(ship)
        elif orientation == "horizontal":
            x, y = reset_ship(ship)

        if debug: print("Placing", ship, orientation, column, row)
        fits = try_ship(ship, orientation, column, row, board)

        if fits:
            if debug: print("Fits")
            canv.move(ship, board_width + x_margin + cell_width * column - x,
                      board_height + y_margin + cell_height * row - y)
            board.append((ship, orientation, column, row))
            ships_right.remove(ship)

        if not fits:
            if debug: print("Doesn't fit")
            continue

    seek_lock_0 = 0  # Enable player to seek
    pass