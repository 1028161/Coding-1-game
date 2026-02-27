# Good Luck!
# The goals for this phase include:
# - Pick out some icons for your game
# - Establish a starting position for each icon
# - Pick a size for your playing space
# - Print your playing space with starting position of each icon

# To make this work, you may have to type this into the terminal --> pip install curses
import curses

game_data = {
    'width': 9,
    'height': 9,
    'player': {"x": 0, "y": 0, "score": 0, "energy": 10, "max_energy": 10},
    'collectibles': [
        {"x": 2, "y": 1, "collected": False},
    ],
    'obstacles': [
        {"x": 2, "y": 7},
        {"x": 8, "y": 3},
        {"x": 1, "y": 5},
        {"x": 4, "y": 9}

    ],

    # ASCII icons
    'snake': "\U0001F7E9",
    'obstacle': "\U0001FAA8 ",
    'apple': "\U0001F34E",
    'empty': "  "
}

def draw_board(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    stdscr.clear()
    for y in range(game_data['height']):
        row = ""
        for x in range(game_data['width']):
            # Player
            if x == game_data['player']['x'] and y == game_data['player']['y']:
                row += game_data['snake']
            # Eagle
            elif x == game_data['eagle_pos']['x'] and y == game_data['eagle_pos']['y']:
                row += game_data['eagle_icon']
            # Obstacles
            elif any(o['x'] == x and o['y'] == y for o in game_data['obstacles']):
                row += game_data['obstacle']
            # Collectibles
            elif any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
                row += game_data['leaf']
            else:
                row += game_data['empty']
        stdscr.addstr(y, 0, row, curses.color_pair(1))

    stdscr.refresh()
    stdscr.getkey()  # pause so player can see board

curses.wrapper(draw_board)