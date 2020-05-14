from header import *

def bot_move():

    def make_heatmap():

        # Ship here == length of ship!!!!!1

        # One instance of a potential board:
        # Called for every ship

        # List ((length, orientation, column, row),
        #       (length, orientation, column, row),
        #       (length, orientation, column, row),
        #       (length, orientation, column, row),
        #       (length, orientation, column, row),
        #       (length, orientation, column, row),
        #       (length, orientation, column, row))

        # saved_placements: list of board-lists

        # heatmap: adds a shade to each coordinate --> list of ((x, y), shade)

        def get_coords(ship, orientation, column, row):
            coords = []
            if orientation == "horizontal":
                for k in range(ship):
                    coords.append((column + k, row))
            elif orientation == "vertical":
                for k in range(ship):
                    coords.append((column, row + k))
            return coords

        def try_ship(ship, orientation, column, row, board):
            global misses_1
            global hits_1

            board_coords = []

            false_report = False
            if len(board) == 0:
                pass
            else:
                lengths = []
                for placed_ship in board:
                    placed_length, placed_orientation, placed_column, placed_row = placed_ship
                    ship_coords = get_coords(placed_length, placed_orientation, placed_column, placed_row)
                    for coords in ship_coords:
                        board_coords.append(coords)
                    lengths.append(placed_length)

                if lengths.count(2) + int(ship == 2) > 3:
                    if false_report: print("False1")
                    return False
                elif lengths.count(3) + int(ship == 3) > 2:
                    if false_report: print("False2")
                    return False
                elif lengths.count(4) + int(ship == 4) > 1:
                    if false_report: print("False3")
                    return False
                elif lengths.count(5) + int(ship == 5) > 1:
                    if false_report: print("False4")
                    return False

            if orientation == "horizontal":
                for k in range(ship):
                    if (column + k, row) in board_coords or (column + k, row) in misses_1:
                        if false_report: print("False5")
                        return False
                    elif column + k > 10:
                        if false_report: print("False6")
                        return False

            elif orientation == "vertical":
                for k in range(ship):
                    if (column, row + k) in board_coords or (column, row + k) in misses_1:
                        if false_report: print("False7")
                        return False
                    elif row + k > 10:
                        if false_report: print("False8")
                        return False

            return True

        debug = False

        global sunk_ships_1
        global hit_coords  # Coordinates of ship currently under attack so far
        global seek_hit

        heatmap = []
        boards = []

        return_condition = False  # Condition after which the loop ends (updated at the end of each loop)

        while not return_condition:

            new_board = False
            ships = [2, 2, 2, 3, 3, 4, 5]
            orientations = ["horizontal", "vertical"]
            board = []
            combinations_tried = []

            if debug: print("Sunk ships:", sunk_ships_1)

            for ship in sunk_ships_1:  # Remove already sunk ships from ships to place
                ships.remove(ship)

            if seek_hit:  # If ship is sunk --> seek_hit = False -->
                # Place the hit ship first, then place the others
                def fit_hit_ship(hit_coords):
                    # Return a random possible placement of ship
                    debug = True

                    if debug: print("Hit_coords", hit_coords, len(hit_coords))

                    possible_hit_ships = list(range(max(2, len(hit_coords)+1), 6))  # possible ship lengths of hit coords
                    if debug: print("Possible Hit Ships:", possible_hit_ships)

                    hit_ship = random.choice(possible_hit_ships)

                    if debug: print("Randomly chosen possible ship length:", hit_ship)

                    if len(hit_coords) > 1:
                        x1, y1 = hit_coords[0]
                        x2, y2 = hit_coords[1]
                        if x1 == x2:
                            orientation = "vertical"
                            if debug: print("Same x coord. in hit coords", orientation)
                        elif y1 == y2:
                            orientation = "horizontal"
                            if debug: print("Same y coord. in hit coords", orientation)
                        else:
                            print("ERROR")
                    elif len(hit_coords) == 1:
                        orientation = random.choice(["horizontal", "vertical"])
                        if debug: print("Random orientation choice:", orientation)

                    x_list = []
                    y_list = []
                    for x, y in hit_coords:
                        x_list.append(x)
                        y_list.append(y)

                    if debug: print("X-values in hit coords", x_list)
                    if debug: print("Y-values in hit coords", y_list)

                    column = min(y_list)
                    row = min(x_list)

                    if debug: print("First column:", column)
                    if debug: print("First row:", row)

                    possible_columns = []
                    possible_rows = []

                    diff = 0
                    if column + hit_ship - 1 > 10 and orientation == "horizontal":
                        if debug: print("Hit close to border")
                        diff = column - (10 - hit_ship - 1)
                        column = 10 - hit_ship - 1  # If hit is close to the right border
                        if debug: print("First possible column:", column)
                    elif row + hit_ship - 1 > 10 and orientation == "vertical":
                        if debug: print("Hit close to border")
                        diff = row - (10 - hit_ship - 1)
                        row = 10 - hit_ship - 1
                        if debug: print("First possible row:", row)

                    possible_offsets = list(range(hit_ship - len(hit_coords) + 1 - diff))
                    if debug: print("Possible Offsets:", possible_offsets)

                    for k in possible_offsets:
                        if debug: print("Offset:", k)
                        if orientation == "horizontal":
                            if column - k > 0:
                                if debug: print("Added new possible first column:", column - k, (column - k) > 0)
                                possible_columns.append(column - k)
                            possible_rows.append(row)
                        elif orientation == "vertical":
                            if row - k > 0:
                                if debug: print("Added new possible first row:", row - k, (row - k) > 0)
                                possible_rows.append(row - k)
                            possible_columns.append(column)

                    column = random.choice(possible_columns)
                    row = random.choice(possible_rows)

                    if debug: print("Randomly chosen first column and row", column, row)

                    return (hit_ship, orientation, column, row)

                hit_ship, orientation, column, row = fit_hit_ship(hit_coords)

                board.append((hit_ship, orientation, column, row))
                ships.remove(hit_ship)


            # Starting to fill a board

            while len(ships) > 0:  # while there are still ships to place


                ship = random.choice(ships)
                column = random.randint(1, 10)  # Inclusive 1 and 10
                row = random.randint(1, 10)
                orientation_idx = random.randint(0, 1)
                orientation = orientations[orientation_idx]

                if debug: print("Ship:", ship, orientation, column, row)

                fits = try_ship(ship, orientation, column, row, board)

                if not fits:
                    if debug: print("Doesnt fit")

                    if (orientation, column, row) not in combinations_tried:
                        combinations_tried.append((orientation, column, row))

                    if len(combinations_tried) == 200:  # If gone through all possible placements
                        ships.remove(ship)
                        new_board = True
                        break
                    continue

                if fits:
                    if debug: print("Fits")

                    combinations_tried = []
                    board.append((ship, orientation, column, row))

                    ships.remove(ship)
                    continue

            # Board filled
            # Check for duplicates

            if len(boards) > 0:
                if debug: print("Board full!")
                duplicate = False
                for placed_board in boards:
                    if board == placed_board:
                        duplicate = True
                        if debug: print("DUPLICATE!!")
                if duplicate:
                    continue  # Continue with next board
                elif not duplicate:
                    boards.append(board)
            else:
                if debug: print("Board full!")
                boards.append(board)

            return_condition = (len(boards) == 1000 and not new_board)  # Actual return condition !!

        '''
        if return condition fullfilled
        for i in range(len(boards)):
            print("Board No.", i+1)
            for ship in boards[i]:
                print(ship)
        '''

        for board in boards:
            debug2 = False
            for placed_ship in board:
                placed_length, placed_orientation, placed_column, placed_row = placed_ship
                ship_coords = get_coords(placed_length, placed_orientation, placed_column, placed_row)

                if debug2: print("Ship:", placed_ship, ship_coords)

                for coords in ship_coords:  # For each coordinate of each ship of each board
                    added = False
                    if len(heatmap) > 0:
                        for h_coords, shade in heatmap:  # For each heatmap entry
                            if coords == h_coords:  # If the current entry is for the coords
                                heatmap.remove((coords, shade))
                                shade += 1
                                heatmap.append((coords, shade))
                                added = True
                                break
                    if not added:
                        heatmap.append((coords, 1))

        return heatmap, boards

    def draw_heatmap(heatmap):
        canv.delete("heatmap")

        def normalize_shades():
            nonlocal heatmap
            max = 0
            min = 100000
            for coords, shade in heatmap:
                if shade > 0:
                    print("Shade:", shade, "Max:", max, "Min:", min)
                    if max < shade:
                        max = shade
                        print("New max:", shade)
                    if min > shade:
                        min = shade
                        print("New min:", shade)

            print("Max", max, "Min", min)
            new_heatmap = []
            for coords, shade in heatmap:
                if shade > 0:
                    print("Old shade", shade)
                    shade = round(255*(shade-min)/(max-min))
                    print("New shade", shade)
                    new_heatmap.append((coords, shade))
            return new_heatmap

        heatmap = normalize_shades()

        for i in range(len(heatmap)):
            (column, row), shade = heatmap[i]
            hex_val = "#%02x%02x%02x" % (shade, shade, shade)
            canv.create_rectangle((board_width + x_margin + cell_width + (column-1) * cell_width,
                                   y_margin + cell_height + (row-1) * cell_height),
                                  (board_width + x_margin + cell_width + column * cell_width,
                                   y_margin + cell_height + row * cell_height), fill=hex_val, tag="heatmap")
            canv.tag_lower("heatmap")

    def make_move(heatmap):
        debug = True
        global seek_hit
        global hit_coords
        global hits_1
        global misses_1

        # If previous move hit --> only look for max in neighbors
        if seek_hit:
            if debug: print("Seek Hit!")
            curr_hit_coords = []
            for coords in hit_coords:
                curr_hit_coords.append(coords)

            if debug: print("Coords of current hits:", curr_hit_coords)

            max_neighbors = []
            for x, y in curr_hit_coords:
                left = 0
                right = 0
                top = 0
                bottom = 0
                if not x == 1: left = 1
                if not x == 10: right = 1

                if not y == 1: top = 1
                if not y == 10: bottom = 1

                if left and ((x-1, y) not in hits_1) and ((x-1, y) not in misses_1):
                    max_neighbors.append((x-1, y))
                    if debug: print("Left possible")
                if right and ((x+1, y) not in hits_1) and ((x+1, y) not in misses_1):
                    max_neighbors.append((x+1, y))
                    if debug: print("Right possible")
                if top and ((x, y-1) not in hits_1) and ((x, y-1) not in misses_1):
                    max_neighbors.append((x, y-1))
                    if debug: print("Top possible")
                if bottom and ((x, y+1) not in hits_1) and ((x, y+1) not in misses_1):
                    max_neighbors.append((x, y+1))
                    if debug: print("Bottom possible")

            if debug: print("Neighbors:", max_neighbors)
            max = 0
            for coords, shade in heatmap:
                if coords in max_neighbors:
                    if shade >= max:
                        max = shade
                        move_coords = coords

            if debug: print("Max neighbor shade:", shade)
            if debug: print("Coords of max shade", move_coords)

        if not seek_hit:  # If normal move
            if debug: print("Not seek hit")
            max = 0
            for coords, shade in heatmap:
                if shade > max:
                    max = shade

            if debug: print("Max shade:", max)
            # Max Shade found at this point

            # Choose move coordinates of max_shade_coords
            max_shade_coords = []
            for coords, shade in heatmap:
                if shade == max:
                    max_shade_coords.append(coords)

            if debug: print("Coords with max shade:", max_shade_coords)
            move_coords = random.choice(max_shade_coords)

            if debug: print("Choosen coords:", move_coords)

        if debug: print("Hits", hits_1, "Misses", misses_1, "move coords", move_coords)
        while move_coords in hits_1 or move_coords in misses_1:
            if debug: print("Already chose that one")
            make_move(heatmap)

        move_x = x_margin + board_width + cell_width * move_coords[0] + int(0.5*cell_width)
        move_y = y_margin + cell_height * move_coords[1] + int(0.5*cell_height)

        mouse.move(move_x, move_y + 44)
        mouse.click(move_x, move_y + 44, 1)

    heatmap, boards = make_heatmap()
    # print("Heatmap", heatmap)
    draw_heatmap(heatmap)
    make_move(heatmap)