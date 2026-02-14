import curses
import time
import random

# Board setup
game_data = {
    'width': 5,
    'height': 5,
    'player': {"x": 0, "y": 0, "score": 0, "energy": 10, "max_energy": 10},
    'eagle_pos': {"x": 4, "y": 4},
    'collectibles': [
        {"x": 2, "y": 1, "collected": False},
    ],
    'obstacles': [
        {"x": 1, "y": 2},
        {"x": 3, "y": 1}
    ],

    # ASCII icons
    'turtle': "\U0001F422",# 🐢
    'eagle_icon': "\U0001F985",# 🦅
    'obstacle': "\U0001FAA8 ",# 🪨
    'leaf': "\U0001F343",# 🍃
    'empty': "..",
}

def draw_board(stdscr):
    stdscr.clear()
    for y in range(game_data['height']):
        row = ""
        for x in range(game_data['width']):
            if game_data['player']["x"] == x and game_data['player']["y"] == y:
                row += game_data['turtle']
            elif game_data['eagle_pos']["x"] == x and game_data['eagle_pos']["y"] == y:
                row += game_data['eagle_icon']
            elif any(o["x"] == x and o["y"] == y for o in game_data['obstacles']):
                row += game_data['obstacle']
            elif any(c["x"] == x and c["y"] == y and not c["collected"] for c in game_data['collectibles']):
                row += game_data['leaf']
            else:
                row += game_data['empty']
        stdscr.addstr(y, 0, row)

    stdscr.addstr(game_data['height'] + 1, 0,
                  f"Score (Moves Survived): {game_data['player']['score']}")
    stdscr.addstr(game_data['height'] + 2, 0,
                  f"Energy: {game_data['player']['energy']}")
    stdscr.addstr(game_data['height'] + 3, 0,
                  "Move with W/A/S/D, Q to quit")
    stdscr.refresh()

def move_eagle():
    directions = [
        (0, -1),  # up
        (0, 1),   # down
        (-1, 0),  # left
        (1, 0)    # right
    ]

    random.shuffle(directions)

    ex = game_data['eagle_pos']["x"]
    ey = game_data['eagle_pos']["y"]

    valid_moves = []

    for dx, dy in directions:
        new_x = ex + dx
        new_y = ey + dy

        # Inside board?
        if not (0 <= new_x < game_data['width'] and
                0 <= new_y < game_data['height']):
            continue

        # Rock collision?
        if any(o["x"] == new_x and o["y"] == new_y
               for o in game_data['obstacles']):
            continue

        valid_moves.append((new_x, new_y))

    # If there are valid moves, pick one
    if valid_moves:
        new_x, new_y = random.choice(valid_moves)
        game_data['eagle_pos']["x"] = new_x
        game_data['eagle_pos']["y"] = new_y

def check_collectibles():
    for c in game_data['collectibles']:
        if (not c["collected"] and
            game_data['player']["x"] == c["x"] and
            game_data['player']["y"] == c["y"]):

            c["collected"] = True
            game_data['player']["energy"] = min(
                game_data['player']["max_energy"],
                game_data['player']["energy"] + 5
            )

def move_player(key):
    key = key.lower()
    px = game_data['player']["x"]
    py = game_data['player']["y"]

    new_x, new_y = px, py

    if key == "w" and py > 0:
        new_y -= 1
    elif key == "s" and py < game_data['height'] - 1:
        new_y += 1
    elif key == "a" and px > 0:
        new_x -= 1
    elif key == "d" and px < game_data['width'] - 1:
        new_x += 1
    else:
        return False

    # Check obstacle collision
    if any(o["x"] == new_x and o["y"] == new_y for o in game_data['obstacles']):
        return False

    game_data['player']["x"] = new_x
    game_data['player']["y"] = new_y

    # Energy decreases per move
    game_data['player']["energy"] -= 1

    # Score increases per move survived
    game_data['player']["score"] += 1

    return True

def spawn_leaf():
    # Limit number of leaves on board
    active_leaves = [c for c in game_data['collectibles'] if not c["collected"]]
    if len(active_leaves) >= 3:
        return

    # 20% chance each turn
    if random.random() > 0.2:
        return

    while True:
        x = random.randint(0, game_data['width'] - 1)
        y = random.randint(0, game_data['height'] - 1)

        # Must not spawn on player, eagle, rock, or existing leaf
        if (x == game_data['player']["x"] and y == game_data['player']["y"]):
            continue

        if (x == game_data['eagle_pos']["x"] and y == game_data['eagle_pos']["y"]):
            continue

        if any(o["x"] == x and o["y"] == y for o in game_data['obstacles']):
            continue

        if any(c["x"] == x and c["y"] == y and not c["collected"]
               for c in game_data['collectibles']):
            continue

        # Valid location found
        game_data['collectibles'].append({
            "x": x,
            "y": y,
            "collected": False
        })
        break

def play_game(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    draw_board(stdscr)

    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key:
            if key.lower() == "q":
                break

            moved = move_player(key)

            if moved:
                check_collectibles()
                move_eagle()
                spawn_leaf()

                # Check lose conditions
                if game_data['player']["energy"] <= 0:
                    break

                if (game_data['player']["x"] == game_data['eagle_pos']["x"] and
                    game_data['player']["y"] == game_data['eagle_pos']["y"]):
                    break

                draw_board(stdscr)

        time.sleep(0.1)

    stdscr.clear()
    stdscr.addstr(2, 2, "GAME OVER")
    stdscr.addstr(3, 2, f"Final Score (Moves Survived): {game_data['player']['score']}")
    stdscr.refresh()
    time.sleep(3)

curses.wrapper(play_game)
