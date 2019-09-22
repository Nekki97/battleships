from tkinter import Tk, Canvas, Button
import random
from pymouse import PyMouse
import math

root = Tk()

# ******************* ONLY IMPORTANT PARAMETERS****************
cell_size = 20
how_many_players = 1 # 1 or 2

# ************ RELATIVE PARAMETERS ***********
cell_width = cell_size
cell_height = cell_size
x_margin = int(0.125 * cell_width)
y_margin = int(0.125 * cell_height)

ship_width = cell_height - 3 * y_margin

board_width = 11 * cell_width + 2 * x_margin
board_height = 11 * cell_height + 2 * y_margin
# ********************************************

# Initialize locks
lock_0 = 0  # Ships placeable on the left
lock_1 = 1  # Ships not placeable on the right
seek_lock_0 = 1  # Ships not seekable on the left
seek_lock_1 = 1  # Ships not seekable on the right

# Initialize Curr_ship to 0 --> no ship
curr_ship = 0

ships = ("five_left", "five_right", "four_left", "four_right", "first_three_left", "second_three_left",
         "first_three_right", "second_three_right", "first_two_left", "second_two_left", "third_two_left",
         "first_two_right", "second_two_right", "third_two_right")

# Initialize Button to say "Start"
button_text_idx_0 = 0
button_text_idx_1 = 0

hits_0 = []  # Hits of left player
hits_1 = []  # Hits of right player
misses_0 = []  # Misses of left player
misses_1 = []  # Misses of right player

player = 0  # player 0 starts

on_grid = False
drop_counter = 0

sunk_ships_0 = []  # Ships of left player that sunk
sunk_ships_1 = []  # Ships of right player that sunk
# TODO: when one player wins --> Win Screen

seek_hit = 0  # Mode after bot hits --> until sunk
hit_coords = []
exact_hit_coords_0 = []
exact_hit_coords_1 = []

canv = Canvas(root, width=2 * board_width, height=2 * board_height + 5 * cell_height)
canv.pack()

mouse = PyMouse()


def next_player():

    global player
    global lock_0
    global lock_1
    global seek_lock_0
    global seek_lock_1
    global how_many_players

    if how_many_players == 1:  # Singleplayer mode
        if lock_0 == 1 and seek_lock_0 == 0:  # After the computer has stopped placing his ships (after lock_1 turns to 1)
            seek_lock_1 = 1
            bot_move()
            seek_lock_0 = 0

    elif how_many_players == 2:  # Two-Player mode

        player = 1 - player
        seek_lock_0 = 1 - seek_lock_0
        seek_lock_1 = 1 - seek_lock_1

        canv.delete("cover")
        canv.create_rectangle(((1-player) * board_width, 0),
                              (board_width + (1-player) * board_width, 2 * board_height+5 * cell_height),
                              fill="black", tag="cover")


def get_middle_coords(ship):
    horizontal = get_orientation(ship)
    curr_x = 0
    curr_y = 0
    if "five" in ship:
        index = 2
        curr_x = (canv.coords(canv.find_withtag(ship)[index])[4] + canv.coords(canv.find_withtag(ship)[index])[0]) / 2
        curr_y = (canv.coords(canv.find_withtag(ship)[index])[5] + canv.coords(canv.find_withtag(ship)[index])[1]) / 2

    if "four" in ship:
        if horizontal:
            index = 1
            curr_x = canv.coords(canv.find_withtag(ship)[index])[4]
            curr_y = (canv.coords(canv.find_withtag(ship)[index])[5] + canv.coords(canv.find_withtag(ship)[index])[1])/2

        if not horizontal:
            index = 1
            curr_x = (canv.coords(canv.find_withtag(ship)[index])[2] + canv.coords(canv.find_withtag(ship)[index])[0])/2
            curr_y = canv.coords(canv.find_withtag(ship)[index])[5]

    if "three" in ship:
        index = 1
        curr_x = (canv.coords(canv.find_withtag(ship)[index])[4]+canv.coords(canv.find_withtag(ship)[index])[0])/2
        curr_y = (canv.coords(canv.find_withtag(ship)[index])[5]+canv.coords(canv.find_withtag(ship)[index])[1])/2

    if "two" in ship:
        if horizontal:
            index = 0
            curr_x = canv.coords(canv.find_withtag(ship)[index])[0]
            curr_y = canv.coords(canv.find_withtag(ship)[index])[3]
        if not horizontal:
            index = 0
            curr_x = canv.coords(canv.find_withtag(ship)[index])[2]
            curr_y = canv.coords(canv.find_withtag(ship)[index])[1]

    return curr_x, curr_y


def get_length(ship):
    k = 0
    if "five" in ship:
        k = 5
    if "four" in ship:
        k = 4
    if "three" in ship:
        k = 3
    if "two" in ship:
        k = 2
    return k


def get_box(ship):
    k = get_length(ship)
    curr_x, curr_y = get_middle_coords(ship)
    horizontal = get_orientation(ship)
    x1, y1, x2, y2 = 0, 0, 0, 0
    if horizontal:
        x1 = int(curr_x - k/2*cell_width)
        x2 = x1 + k*cell_width
        y1 = curr_y - cell_height/2
        y2 = y1 + cell_height

    if not horizontal:
        x1 = curr_x - cell_width/2
        x2 = x1 + cell_width
        y1 = curr_y - k/2 * cell_height
        y2 = y1 + k * cell_height

    return x1, y1, x2, y2


def get_orientation(ship):
    horizontal = True
    index = 0
    if "five" in ship:
        index = 2
    if "four" in ship:
        index = 1
    if "three" in ship:
        index = 1
    if "two" in ship:
        index = 0

    if canv.coords(canv.find_withtag(ship)[index])[0] - \
            canv.coords(canv.find_above(canv.find_withtag(ship)[index]))[0] == 0 and "two" not in ship:
        horizontal = False
    if canv.coords(canv.find_withtag(ship)[index])[3] - \
            canv.coords(canv.find_above(canv.find_withtag(ship)[index]))[3] != 0 and "two" in ship:
        horizontal = False

    return horizontal


def get_current_ship():
    global ships
    for ship in ships:
        for i in range(len(canv.find_withtag(ship))):
            if not len(canv.find_withtag("current")) == 0:
                if canv.find_withtag("current")[0] == canv.find_withtag(ship)[i]:
                    return ship
    return 0


def flip_ship(ship):
    tag = ship
    curr_x, curr_y = get_middle_coords(ship)

    if curr_x > board_width:
        right = 1
    else:
        right = 0

    horizontal = get_orientation(ship)

    k = get_length(ship)

    x, y = 0, 0
    if horizontal:
        x = curr_x - cell_width / 2
        y = curr_y - ((k) / 2) * cell_height
    if not horizontal:
        x = curr_x - ((k) / 2) * cell_width
        y = curr_y - cell_height / 2

    min_x = x_margin + cell_width + right * board_width
    max_x = 2 * board_width
    min_y = y_margin + cell_height + right * board_height
    max_y = 2 * board_height

    if x < min_x: x = min_x
    if x + k * cell_width > max_x: x = max_x - k * cell_width
    if y < min_y: y = min_y
    if y + k * cell_height > max_y: y = max_y - k * cell_height

    horizontal = 1 - horizontal
    canv.delete(ship)
    print_ship(x, y, tag, horizontal)
    return x, y


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


def buttons():

    def start_reset_0():

        global lock_0
        global lock_1
        global seek_lock_0
        global seek_lock_1
        global ships
        global button_text_idx_0
        global button_text_idx_1

        if button_text_idx_0 == 0:
            # Start Button

            if how_many_players == 2:
                # TODO look into this
                seek_lock_0 = 0
                seek_lock_1 = 0
                lock_1 = 0  # Enable ship placing for player 2

            next_player()  # No effect on Singleplayer mode at this point
            lock_0 = 1  # Disable ship placing for player (1)
            button_text_idx_0 = 1  # Change text to reset

            if how_many_players == 1:
                bot_place()

        elif button_text_idx_0 == 1:
            # Reset Button
            for ship in ships:
                x, y, = reset_ship(ship)
            canv.delete("miss")
            canv.delete("hit")
            canv.delete("heatmap")
            lock_0 = 0
            lock_1 = 1
            seek_lock_0 = 1
            seek_lock_1 = 1
            button_text_idx_0 = 0
            button_text_idx_1 = 0

        # Update the Button with new name
        buttons()

    def start_reset_1():

        global lock_0
        global lock_1
        global seek_lock_0
        global seek_lock_1
        global ships
        global button_text_idx_0
        global button_text_idx_1

        # TODO: fix this

        if button_text_idx_1 == 0:
            # Start Button
            lock_0 = 1 # to lock it next turn
            lock_1 = 1
            seek_lock_0 = 1 # set to 0 after next_player()
            seek_lock_1 = 0
            next_player()
            button_text_idx_1 = 1

        elif button_text_idx_1 == 1:
            # Reset Button
            for ship in ships:
                print("reset 4")
                x, y = reset_ship(ship)
            canv.delete("miss")
            canv.delete("hit")
            lock_0 = 0
            lock_1 = 0
            seek_lock_0 = 1
            seek_lock_1 = 1
            button_text_idx_0 = 0
            button_text_idx_1 = 0

        # Update the Button with new name
        buttons()

    global button_text_idx_0
    global button_text_idx_1
    button_texts = ["Start", "Reset"]
    button_text_0 = button_texts[button_text_idx_0]
    button_text_1 = button_texts[button_text_idx_1]

    # Left player buttons
    button0 = Button(root, text=button_text_0, command=start_reset_0, bd=4, bg='#001d26')
    button0.place(x=x_margin+cell_width, y=2*board_height+int(3.5*cell_height), height=ship_width, width=3*cell_width)
    root.bind(button0, "<ButtonPress-1>", start_reset_0)

    if how_many_players == 2:
        # Right player buttons
        button1 = Button(root, text=button_text_1, command=start_reset_1, bd=4, bg='#001d26')
        button1.place(x=board_width + x_margin + cell_width, y=2 * board_height + int(3.5 * cell_height), height=ship_width,
                      width=3 * cell_width)
        root.bind(button1, "<ButtonPress-1>", start_reset_1)


def reset_ship(ship):
    i = 0
    if "right" in ship:
        i = 1

    x, y = 0, 0
    if "five" in ship:
        x = x_margin + cell_width + i * board_width
        y = 2 * board_height
    if "four" in ship:
        x = x_margin + cell_width + i * board_width + 5 * cell_width
        y = 2 * board_height
    if "first_three" in ship:
        x = x_margin + cell_width + i * board_width
        y = 2 * board_height + cell_height
    if "second_three" in ship:
        x = x_margin + cell_width + i * board_width + 3 * cell_width
        y = 2 * board_height + cell_height
    if "first_two" in ship:
        x = x_margin + cell_width + i * board_width + 6 * cell_width
        y = 2 * board_height + cell_height
    if "second_two" in ship:
        x = x_margin + cell_width + i * board_width + 8 * cell_width
        y = 2 * board_height + cell_height
    if "third_two" in ship:
        x = x_margin + cell_width + i * board_width
        y = 2 * board_height + 2 * cell_height

    canv.delete(ship)
    print_ship(x, y, ship, True)

    return x, y


def print_ship(x, y, tag, hor):
    right = 0
    if "right" in tag:
        right = 1

    color = "green"
    if right:
        color = "yellow"

    length = get_length(tag)

    if hor:
        canv.create_polygon(((x + cell_width, y + int(cell_height-ship_width)/2), (x, y + cell_height / 2),
                             (x + cell_width, y + int(cell_height-ship_width)/2 + ship_width)),
                            fill=color, outline="black", tag=tag)

        for i in range(0, length - 2):
            canv.create_polygon((x + cell_width * (i + 1), y + int(cell_height-ship_width)/2),
                                (x + cell_width * (i + 1), y + int(cell_height-ship_width)/2 + ship_width),
                                (x + cell_width * (i + 2), y + int(cell_height-ship_width)/2 + ship_width),
                                (x + cell_width * (i + 2), y + int(cell_height-ship_width)/2),
                                fill=color, outline="black", tag=tag)

        canv.create_polygon(((x + (length - 1) * cell_width, y + int(cell_height-ship_width)/2),
                             (x + length * cell_width, y + cell_height / 2),
                             (x + (length - 1) * cell_width, y + int(cell_height-ship_width)/2 + ship_width)),
                            fill=color, outline="black", tag=tag)

    if not hor:
        canv.create_polygon((x + int(cell_width-ship_width)/2, y + cell_height), (x + cell_width / 2, y),
                            (x + cell_width - int(cell_width-ship_width)/2, y + cell_height),
                            fill=color, outline="black", tag=tag)

        for i in range(length - 2):
            canv.create_polygon(((x + int(cell_width-ship_width)/2, y + (i + 1) * cell_height),
                                 (x + cell_width - int(cell_width-ship_width)/2, y + (i + 1) * cell_height),
                                 (x + cell_width - int(cell_width-ship_width)/2, y + (i + 2) * cell_height),
                                 (x + int(cell_width-ship_width)/2, y + (i + 2) * cell_height)),
                                fill=color, outline="black", tag=tag)

        canv.create_polygon(((x + int(cell_width-ship_width)/2, y + (length - 1) * cell_height),
                             (x + cell_width / 2, y + length * cell_height),
                             (x + cell_width - int(cell_width-ship_width)/2, y + (length - 1) * cell_height)),
                            fill=color, outline="black", tag=tag)


def print_board():
    global how_many_players
    old_tags = ("five_", "four_", "first_three_", "second_three_", "first_two_", "second_two_", "third_two_")

    for i in (0, 1):
        tags = []
        if i:
            suffix = "right"
        else:
            suffix = "left"
        for tag in old_tags:
            tags.append(tag + suffix)

        for k in (0, 1):
            for j in range(12):
                canv.create_line(i * board_width + j * cell_width + x_margin,
                                 k * board_height + y_margin,
                                 i * board_width + j * cell_width + x_margin,
                                 k * board_height + board_height - y_margin, fill='black')

                canv.create_line(i * board_width + x_margin,
                                 k * board_height + j * cell_height + y_margin,
                                 i * board_width + board_width - x_margin,
                                 k * board_height + j * cell_height + y_margin, fill='black')

            letters = "ABCDEFGHIJ"
            for j in range(10):
                canv.create_text(i * board_width + x_margin + cell_width / 2,
                                 k * board_height + y_margin + (j + 1) * cell_height + cell_height / 2,
                                 font=("Purisa", int(3/4*cell_height)), text=letters[j])

                canv.create_text(i * board_width + x_margin + (j + 1) * cell_width + cell_width / 2,
                                 k * board_height + y_margin + cell_height / 2,
                                 font=("Purisa", int(3/4*cell_height)), text=str(j + 1))

        print_ship(x_margin + cell_width + i * board_width, 2 * board_height,
                   tags[0], True)
        print_ship(x_margin + cell_width + i * board_width + 5 * cell_width, 2 * board_height,
                   tags[1], True)

        print_ship(x_margin + cell_width + i * board_width, 2 * board_height + cell_height,
                   tags[2], True)
        print_ship(x_margin + cell_width + i * board_width + 3 * cell_width, 2 * board_height + cell_height,
                   tags[3], True)
        print_ship(x_margin + cell_width + i * board_width + 6 * cell_width, 2 * board_height + cell_height,
                   tags[4], True)
        print_ship(x_margin + cell_width + i * board_width + 8 * cell_width, 2 * board_height + cell_height,
                   tags[5], True)

        print_ship(x_margin + cell_width + i * board_width, 2 * board_height + 2 * cell_height,
                   tags[6], True)

    # Separating Line
    canv.create_line(board_width, 0, board_width, 2 * board_height + 5 * cell_height)

    if how_many_players == 2:
        canv.create_rectangle((board_width, 0), (2 * board_width, 2*board_height+5*cell_height),
                              fill="black", tag="cover")

    root.geometry('+%d+%d' % (0, 0))
    root.mainloop()


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


def initialize_bindings():
    dm = DragManager()
    dm.add_draggable(canv)
    buttons()
    root.bind("<ButtonPress-1>", seek_and_destroy)


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