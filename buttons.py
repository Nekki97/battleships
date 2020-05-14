from game_funcs import *
from bot_place import *


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