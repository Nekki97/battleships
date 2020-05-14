from bot_move import *
from ship_funcs import *
from dragManager import *
from buttons import *
from seek_n_destroy import *


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


def initialize_bindings():
    dm = DragManager()
    dm.add_draggable(canv)
    buttons()
    root.bind("<ButtonPress-1>", seek_and_destroy)
