import curses
import random

# Constants for the game
KEY_UP = curses.KEY_UP
KEY_DOWN = curses.KEY_DOWN
KEY_LEFT = curses.KEY_LEFT
KEY_RIGHT = curses.KEY_RIGHT

# Display characters
SNAKE_CHAR = '#'
FOOD_CHAR = '*'

# Color pair identifiers
SNAKE_COLOR = 1
FOOD_COLOR = 2
BORDER_COLOR = 3
MESSAGE_COLOR = 4


def main(stdscr):
    curses.curs_set(0)  # hide cursor
    stdscr.nodelay(1)   # non-blocking input
    stdscr.keypad(1)    # enable arrow keys

    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(SNAKE_COLOR, curses.COLOR_GREEN, -1)
        curses.init_pair(FOOD_COLOR, curses.COLOR_RED, -1)
        curses.init_pair(BORDER_COLOR, curses.COLOR_CYAN, -1)
        curses.init_pair(MESSAGE_COLOR, curses.COLOR_YELLOW, -1)

    height, width = stdscr.getmaxyx()
    box = [[3,3], [height-3, width-3]]

    # Draw game border
    for y in range(box[0][0], box[1][0] + 1):
        stdscr.addch(y, box[0][1], curses.ACS_VLINE, curses.color_pair(BORDER_COLOR))
        stdscr.addch(y, box[1][1], curses.ACS_VLINE, curses.color_pair(BORDER_COLOR))
    for x in range(box[0][1], box[1][1] + 1):
        stdscr.addch(box[0][0], x, curses.ACS_HLINE, curses.color_pair(BORDER_COLOR))
        stdscr.addch(box[1][0], x, curses.ACS_HLINE, curses.color_pair(BORDER_COLOR))
    stdscr.refresh()

    # Initial snake and food
    snake = [[height//2, width//2 + 1], [height//2, width//2], [height//2, width//2 - 1]]
    direction = KEY_RIGHT
    food = [random.randint(box[0][0]+1, box[1][0]-1), random.randint(box[0][1]+1, box[1][1]-1)]
    stdscr.addch(food[0], food[1], FOOD_CHAR, curses.color_pair(FOOD_COLOR))

    score = 0
    while True:
        event = stdscr.getch()
        if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            # Avoid reversing direction directly
            opposite = {KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP, KEY_LEFT: KEY_RIGHT, KEY_RIGHT: KEY_LEFT}
            if event != opposite.get(direction):
                direction = event

        head = snake[0].copy()
        if direction == KEY_UP:
            head[0] -= 1
        elif direction == KEY_DOWN:
            head[0] += 1
        elif direction == KEY_LEFT:
            head[1] -= 1
        elif direction == KEY_RIGHT:
            head[1] += 1

        # Collision with border or self
        if (head[0] in [box[0][0], box[1][0]] or
            head[1] in [box[0][1], box[1][1]] or
            head in snake):
            msg = f"Game Over! Score: {score}"
            stdscr.nodelay(0)
            stdscr.addstr(height//2, width//2 - len(msg)//2, msg, curses.color_pair(MESSAGE_COLOR))
            stdscr.getch()
            break

        snake.insert(0, head)

        if head == food:
            score += 1
            food = None
            while food is None:
                nf = [random.randint(box[0][0]+1, box[1][0]-1),
                      random.randint(box[0][1]+1, box[1][1]-1)]
                if nf not in snake:
                    food = nf
            stdscr.addch(food[0], food[1], FOOD_CHAR, curses.color_pair(FOOD_COLOR))
        else:
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')

        stdscr.addch(head[0], head[1], SNAKE_CHAR, curses.color_pair(SNAKE_COLOR))
        stdscr.addstr(box[0][0]-1, box[0][1], f"Score: {score} ", curses.color_pair(MESSAGE_COLOR))
        stdscr.refresh()
        curses.napms(100)

if __name__ == "__main__":
    curses.wrapper(main)
