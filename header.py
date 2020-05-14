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