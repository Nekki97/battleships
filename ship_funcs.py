from header import *

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