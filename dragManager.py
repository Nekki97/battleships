from ship_funcs import *

class DragManager:

    def add_draggable(self, widget):
        widget.bind("<ButtonPress-1>", self.on_start)
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor="hand")

    def on_start(self, event):
        ship = get_current_ship()
        if ship != 0:
            canv.tag_raise(ship)
        pass

    def on_drag(self, event):

        if (event.x < board_width and not lock_0) or (event.x > board_width and not lock_1):
            global right
            global max_border_x
            global min_border_x
            global max_border_y
            global min_border_y
            global curr_ship

            ship = get_current_ship()

            if ship != 0:

                def key(event):
                    global on_grid
                    global drop_counter

                    if event.char == "f":
                        drop_counter = 0
                        on_grid = True  # Disable automatic grid placement when flipping

                        ship = get_current_ship()

                        x, y = flip_ship(ship)

                        curr_x, curr_y = get_middle_coords(ship)

                        mouse.release(curr_x, curr_y + 44, 1)
                        mouse.press(curr_x, curr_y + 44, 1)

                curr_ship = ship
                curr_x, curr_y = get_middle_coords(ship)

                k = get_length(ship)

                half = (k * cell_width) / 2

                right = 0
                if "right" in ship:
                    right = 1

                new_x = event.x - curr_x
                new_y = event.y - curr_y

                max_border_x = board_width + right * board_width - x_margin
                max_border_y = 2 * board_height + 3 * cell_height
                min_border_x = cell_width + x_margin + right * board_width
                min_border_y = board_height + cell_height + y_margin

                horizontal = get_orientation(ship)

                if horizontal:
                    if event.x + half > max_border_x:
                        new_x = max_border_x - half - curr_x
                    if event.x - half < min_border_x:
                        new_x = min_border_x + half - curr_x
                    if event.y + ship_width/2 > max_border_y:
                        new_y = max_border_y - ship_width/2 - curr_y
                    if event.y - ship_width/2 < min_border_y:
                        new_y = min_border_y + ship_width/2 - curr_y

                if not horizontal:
                    if event.x + ship_width/2 > max_border_x:
                        new_x = max_border_x - ship_width/2 - curr_x
                    if event.x - ship_width/2 < min_border_x:
                        new_x = min_border_x + ship_width/2 - curr_x
                    if event.y + half > max_border_y:
                        new_y = max_border_y - half - curr_y
                    if event.y - half < min_border_y:
                        new_y = min_border_y + half - curr_y

                canv.move(ship, new_x, new_y)
                root.bind("<Key>", key)

    def on_drop(self, event):
        global curr_ship
        global on_grid
        global drop_counter

        drop_counter += 1

        # print("Drop counter", drop_counter, "on_grid", on_grid)

        if (not on_grid) or (on_grid and drop_counter == 2):
            drop_counter = 0
            on_grid = False

            if (event.x < board_width and not lock_0) or (event.x > board_width and not lock_1):

                ship = curr_ship

                if ship != 0:

                    curr_x, curr_y = get_middle_coords(ship)
                    k = get_length(ship)

                    # Unbind "F" key to not flip placed ships
                    root.unbind("<Key>")

                    horizontal = get_orientation(ship)

                    min_x = x_margin + cell_width + right * board_width
                    min_y = board_height + y_margin + cell_height

                    column = int((curr_x - min_x) / cell_width) + 1
                    row = int((curr_y - min_y) / cell_height) + 1

                    if ("four" in ship or "two" in ship) and horizontal:
                        column = int((curr_x - min_x + cell_width/2) / cell_width) + 1

                    if ("four" in ship or "two" in ship) and not horizontal:
                        row = int((curr_y - min_y + cell_height/2) / cell_height) + 1

                    # Resets Ship if placed outside grid, places it otherwise
                    if (horizontal and column + k/2 - 1 <= 10 and row <= 10) or \
                            (not horizontal and column <= 10 and row + k/2 - 1 <= 10):

                        new_x = min_x + (column - 1) * cell_width + cell_width / 2 - curr_x
                        new_y = min_y + (row - 1) * cell_height + cell_height / 2 - curr_y

                        if ("four" in ship or "two" in ship) and horizontal:
                            new_x = min_x + (column - 1) * cell_width - curr_x

                        if ("four" in ship or "two" in ship) and not horizontal:
                            new_y = min_y + (row - 1) * cell_height - curr_y

                        canv.move(ship, new_x, new_y)

                    else:
                        x, y = reset_ship(ship)

                    # Resets Ship if it overlaps with any other ship
                    x1, y1, x2, y2 = get_box(ship)
                    for i in canv.find_overlapping(x1+1, y1+1, x2-1, y2-1):
                        for j in canv.gettags(i):
                            if j != ship and j != "current":
                                x, y = reset_ship(ship)
                                return
                            else:
                                continue