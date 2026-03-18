# Good Luck!
# The goals for this phase include:
# - Pick out some icons for your game
# - Establish a starting position for each icon
# - Pick a size for your playing space
# - Print your playing space with starting position of each icon

# To make this work, you may have to type this into the terminal --> pip install curses
import curses
import random
import time


game_data = {
    'width': 9,
    'height': 9,
    'player': {"x": 0, "y": 0, "score": 0, 'current_direction': "S"},
    'collectibles': [
        {"x": 2, "y": 1, "collected": False},
    ],
    'obstacles': [
        {"x": 7, "y": 3},
        {"x": 4, "y": 1},
        {"x": 3, "y": 8},
        {"x": 2, "y": 5},
        {"x": 6, "y": 6},
        {"x": 1, "y": 2}

    ],
    'collided': False,

    # ASCII icons
    'snake': "\U0001F7E9",
    'obstacle': "\U0001FAA8 ",
    'apple': "\U0001F34E",
    'empty': "  "
}

def collided():
    x = game_data['player']['x']
    y = game_data['player']['y']
    if any(o['x'] == x and o['y'] == y for o in game_data['obstacles']):
        return True

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
            # Obstacles
            elif any(o['x'] == x and o['y'] == y for o in game_data['obstacles']):
                row += game_data['obstacle']
            # Collectibles
            elif any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
                row += game_data['apple']
            else:
                row += game_data['empty']
        stdscr.addstr(y, 0, row, curses.color_pair(1))

#___________________________________________________________
    stdscr.addstr(game_data['height'] + 1, 0,
                  f"Moves Survived: {game_data['player']['score']}",
                  curses.color_pair(1))
    stdscr.addstr(game_data['height'] + 2, 0,
                  "Move with W/A/S/D, Q to quit",
                  curses.color_pair(1))
    stdscr.refresh()

def move_player():
    x = game_data['player']['x']
    y = game_data['player']['y']
    new_x, new_y = x, y
    #key = key.lower()

    if game_data['player']['current_direction'] == "N" and y > 0:
        new_y -= 1
    elif game_data['player']['current_direction'] == "S" and y < game_data['height'] - 1:
        new_y += 1
    elif game_data['player']['current_direction'] == "W" and x > 0:
        new_x -= 1
    elif game_data['player']['current_direction'] == "E" and x < game_data['width'] - 1:
        new_x += 1
    else:
        return  # Invalid key or move off board
    
        # Check for obstacles
    if any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
        return

    # Update position and increment score
    game_data['player']['x'] = new_x
    game_data['player']['y'] = new_y
    game_data['player']['score'] += 1
        
def change_direction(key):
    # Accept both WASD and arrow keys (curses uses KEY_UP/KEY_DOWN/etc)
    if key in ("w", "KEY_UP"):
        game_data['player']['current_direction'] = "N"
    elif key in ("s", "KEY_DOWN"):
        game_data['player']['current_direction'] = "S"
    elif key in ("a", "KEY_LEFT"):
        game_data['player']['current_direction'] = "W"
    elif key in ("d", "KEY_RIGHT"):
        game_data['player']['current_direction'] = "E"


def spawn_apple():
    spawned_apple = [c for c in game_data['collectibles'] if not c['collected']]
    if len(spawned_apple) >= 3:
        return
    if random.random() > 0.2:
        return
    while True:
        x = random.randint(0, game_data['width'] - 1)
        y = random.randint(0, game_data['height'] - 1)
        
        if (x, y) == (game_data['player']['x'], game_data['player']['y']):
            continue
        if any(o['x'] == x and o['y'] == y for o in game_data['obstacles']):
            continue
        if any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
            continue

        game_data['collectibles'].append({"x": x, "y": y, "collected": False})
        break
        
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    draw_board(stdscr)

    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key and key.lower() == "q":
            break

        # Update direction when the player presses a movement key.
        if key:
            change_direction(key.lower())

        # Move automatically each tick in the current direction.
        move_player()
        draw_board(stdscr)
        time.sleep(0.3)
    # stdscr.refresh()
    # stdscr.getkey()  # pause so player can see board
curses.wrapper(main)