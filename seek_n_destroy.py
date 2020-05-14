from game_funcs import *
from ship_funcs import *

def seek_and_destroy(event):

    def add_miss(column, row, right):

        global misses_0
        global misses_1

        canv.create_oval(int(right * board_width + column * cell_width + cell_width/2 + x_margin - cell_height/4),
                         int(row * cell_height + cell_height/2 + y_margin - cell_height/4),
                         int(right * board_width + column * cell_width + cell_width/2 + x_margin + cell_height/4),
                         int(row * cell_height + cell_height/2 + y_margin + cell_height/4),
                         fill="blue", tag="miss")

        canv.create_oval(int((1-right) * board_width + column * cell_width + cell_width / 2 + x_margin - cell_height/4),
                         int(row * cell_height + cell_height / 2 + y_margin + board_height - cell_height / 4),
                         int((1-right) * board_width + column * cell_width + cell_width / 2 + x_margin + cell_height/4),
                         int(row * cell_height + cell_height / 2 + y_margin + board_height + cell_height / 4),
                         fill="blue", tag="miss")

        if right: misses = misses_1
        else: misses = misses_0

        if (column, row) in misses:
            return
        else:
            if right: misses_1.append((column, row))
            elif not right: misses_0.append((column, row))
            next_player()

    def add_hit(column, row, right, ship):

        def check_sunk(ship):

            def mid_point_3(x1, y1, x2, y2, x3, y3):
                min_x = min(x1, x2, x3)
                min_y = min(y1, y2, y3)
                max_x = max(x1, x2, x3)
                max_y = max(y1, y2, y3)
                return (max_x + min_x)/2, (max_y + min_y)/2

            def mid_point_4(x1, y1, x2, y2, x3, y3, x4, y4):
                min_x = min(x1, x2, x3, x4)
                min_y = min(y1, y2, y3, y4)
                max_x = max(x1, x2, x3, x4)
                max_y = max(y1, y2, y3, y4)
                return (max_x + min_x)/2, (max_y + min_y)/2

            global sunk_ships_0
            global sunk_ships_1
            global exact_hit_coords_0
            global exact_hit_coords_1

            mid_points = []
            for i in range(5):
                if len(canv.find_withtag(ship)) > i:
                    length = len(canv.coords(canv.find_withtag(ship)[i]))
                    (mid_x,mid_y) = 0, 0
                    if length == 6:
                        x1, y1, x2, y2, x3, y3 = canv.coords(canv.find_withtag(ship)[i])
                        (mid_x, mid_y) = mid_point_3(x1, y1, x2, y2, x3, y3)
                    elif length == 8:
                        x1, y1, x2, y2, x3, y3, x4, y4 = canv.coords(canv.find_withtag(ship)[i])
                        (mid_x, mid_y) = mid_point_4(x1, y1, x2, y2, x3, y3, x4, y4)
                    mid_points.append((mid_x, mid_y))

            for (x, y) in mid_points:
                if (right and (x, y) not in exact_hit_coords_1) or (not right and (x, y) not in exact_hit_coords_0):
                    return
                continue

            length = get_length(ship)
            if right:
                sunk_ships_0.append(length)
            if not right:
                sunk_ships_1.append(length)
            if len(sunk_ships_0) == 7:
                canv.create_text(cell_width, cell_height, text="Player 1 Wins!")
            if len(sunk_ships_1) == 7:
                canv.create_text(cell_width, cell_height, text="Player 2 Wins!")

            return True

        global hits_0
        global hits_1
        global seek_hit
        global hit_coords

        # On seek and destroy board
        canv.create_line((right * board_width + column * cell_width + x_margin + 1,
                          row * cell_height + y_margin + 1),
                         (right * board_width + (column + 1) * cell_width + x_margin - 1,
                          (row + 1) * cell_height + y_margin - 1),
                         width=2, fill="red", tag="hit")

        canv.create_line((right * board_width + column * cell_width + x_margin + 1,
                          (row + 1) * cell_height + y_margin - 1),
                         (right * board_width + (column + 1) * cell_width + x_margin - 1,
                          row * cell_height + y_margin + 1),
                         width=2, fill="red", tag="hit")
        # On enemy board
        canv.create_line(((1-right) * board_width + column * cell_width + x_margin + 1,
                          row * cell_height + y_margin + board_height + 1),
                         ((1-right) * board_width + (column + 1) * cell_width + x_margin - 1,
                          (row + 1) * cell_height + y_margin + board_height - 1),
                         width=2, fill="red", tag="hit")

        canv.create_line(((1-right) * board_width + column * cell_width + x_margin + 1,
                          (row + 1) * cell_height + y_margin + board_height - 1),
                         ((1-right) * board_width + (column + 1) * cell_width + x_margin - 1,
                          row * cell_height + y_margin + board_height + 1),
                         width=2, fill="red", tag="hit")

        hit_x = (1-right) * board_width + column * cell_width + cell_width/2 + x_margin
        hit_y = row * cell_height + cell_height/2 + y_margin + board_height

        if right and (column, row) not in hits_1:
            hits_1.append((column, row))
            seek_hit = True
            hit_coords.append((column, row))
            exact_hit_coords_1.append((hit_x, hit_y))
        elif not right and (column, row) not in hits_0:
            hits_0.append((column, row))
            exact_hit_coords_0.append((hit_x, hit_y))

        next_player()

        if check_sunk(ship):
            x1, y1, x2, y2 = get_box(ship)
            if not right:
                x1 -= board_width
                x2 -= board_width

            # In own seek and destroy field
            canv.create_rectangle((x1 + right * board_width + 1, y1-board_height + 1),
                                  (x2 + right * board_width, y2-board_height), width=2, tag="hit")

            # On enemy board
            canv.create_rectangle((x1 + (1-right) * board_width + 1, y1 + 1),
                                  (x2 + (1-right) * board_width, y2), width=2, tag="hit")

            seek_hit = False
            hit_coords = []

    def check_ship(column, row, right):
        global ships
        for ship in ships:
            x1, y1, x2, y2 = get_box(ship)
            min_x = right * board_width + x_margin + cell_width
            min_y = board_height + y_margin + cell_height
            column_1 = int((x1-min_x)/cell_width) + 1
            column_2 = int((x2 - min_x) / cell_width) + 1
            row_1 = int((y1 - min_y) / cell_height) + 1
            row_2 = int((y2 - min_y) / cell_height) + 1

            if column_1 <= column < column_2 and row_1 <= row < row_2:
                curr_ship = ship
                return True, curr_ship

        return False, None

    global seek_lock_0
    global seek_lock_1

    if (event.x < board_width and not seek_lock_0) or (event.x > board_width and not seek_lock_1):
        min_x = x_margin + cell_width
        min_y = y_margin + cell_height
        max_x = 2 * board_width
        max_y = board_height
        if min_x < event.x < max_x and min_y < event.y < max_y:
            right = 0
            if event.x > board_width:
                right = 1
                min_x += board_width
            column = int((event.x - min_x)/cell_width) + 1
            row = int((event.y - min_y)/ cell_height) + 1
            if column <= 10 and row <= 10:
                if (not right and not seek_lock_0) or (right and not seek_lock_1):
                    ship_found, ship = check_ship(column, row, 1-right)
                    if ship_found:
                        add_hit(column, row, right, ship)  # returns array of hit-coordinates including new
                    else:
                        add_miss(column, row, right)  # returns array of miss-coordinates including new

        seek_lock_0 = 1 - seek_lock_0  # Flip seeker
        seek_lock_1 = 1 - seek_lock_1  # Flip seeker