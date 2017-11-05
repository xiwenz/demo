import turtle
import random

t = turtle.Turtle()
turtle.tracer(10000, 0.0001)

char_0 = [
    ' *** ',
    '*  **',
    '* * *',
    '**  *',
    '*   *',
    ' *** ',
]
char_1 = [
    '  *  ',
    ' **  ',
    '  *  ',
    '  *  ',
    '  *  ',
    ' *** ',
]
char_2 = [
    ' *** ',
    '*   *',
    '   * ',
    '  *  ',
    ' *   ',
    '*****',
]
char_3 = [
    '*****',
    '    *',
    '  ** ',
    '    *',
    '*   *',
    ' *** ',
]
char_4 = [
    '   * ',
    '  ** ',
    ' * * ',
    '*  * ',
    '*****',
    '   * ',
]
char_5 = [
    '*****',
    '*    ',
    '**** ',
    '    *',
    '*   *',
    ' *** '
]
char_6 = [
    ' *** ',
    '*    ',
    '**** ',
    '*   *',
    '*   *',
    ' *** '
]
char_7 = [
    '*****',
    '    *',
    '   * ',
    '  *  ',
    '  *  ',
    '  *  ',
]
char_8 = [
    ' *** ',
    '*   *',
    ' *** ',
    '*   *',
    '*   *',
    ' *** ',
]
char_9 = [
    ' *** ',
    '*   *',
    '*   *',
    ' ****',
    '    *',
    ' *** ',
]
chars = [char_0, char_1, char_2, char_3, char_4,
         char_5, char_6, char_7, char_8, char_9]

char_girl = [
    ' ** ** ',
    ' ** ** ',
    '       ',
    '  ***  ',
    '    *  ',
    '       ',
]
char_happy = [
    ' ** ** ',
    '*******',
    '*******',
    ' ***** ',
    '  ***  ',
    '   *   ',
]


def setpen(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.setheading(0)


def rect(x, y, l, color, line_color='black'):
    setpen(x, y)
    t.color(line_color)
    t.fillcolor(color)
    t.begin_fill()
    for i in range(4):
        t.forward(l)
        t.right(90)
    t.end_fill()


def draw_char(x, y, a, color, line_color='black'):
    length = 5
    for i, row in enumerate(a):
        offset_y = y - i * length
        for j, c in enumerate(row):
            offset_x = x + j * length
            if c == ' ':
                pass
            else:
                rect(offset_x, offset_y, length, color, line_color)


def bad_ending():
    for girl_coordinate in girl_coordinates:
        girl_x, girl_y = girl_coordinate
        rect(girl_x * 60 - 270, girl_y * 60 - 210, 60, 'white')
        char_x = girl_x * 60 - 270 + (60 - 5 * 5) // 2
        char_y = girl_y * 60 - 210 - (60 - 6 * 5) // 2
        draw_char(char_x, char_y, char_girl, '#F08080')
    global need_new_game
    need_new_game = True


def click(*args):
    x, y = args
    grid_x = int((x+270)//60)
    grid_y = int((y+210)//60) + 1
    global girl_map
    if grid_x == 4 and grid_y == 10:
        new_game()
    elif need_new_game:
        return
    if grid_x not in range(9) or grid_y not in range(9):
        pass
    elif not girl_map[grid_x][grid_y]:
        pass
    elif (grid_x, grid_y) in girl_coordinates:
        bad_ending()
    else:
        calc_number(grid_x, grid_y)
        happy_ending()


def happy_ending():
    if sum(map(lambda row: sum(row), girl_map)) == girl_number:
        draw_char(-17, 375, char_happy, 'red', 'red')
        global need_new_game
        need_new_game = True


def calc_number(grid_x, grid_y):
    count = 0
    global girl_map
    for i in range(-1, 2):
        for j in range(-1, 2):
            if grid_x + i not in range(9) or grid_y + j not in range(9):
                continue
            if (grid_x + i, grid_y + j) in girl_coordinates:
                count += 1
    rect(grid_x * 60 - 270, grid_y * 60 - 210, 60, 'white')
    if count != 0:
        char_x = grid_x * 60 - 270 + (60 - 5 * 5) // 2
        char_y = grid_y * 60 - 210 - (60 - 6 * 5) // 2
        draw_char(char_x, char_y, chars[count], 'black')
    girl_map[grid_x][grid_y] = False


def new_game():
    global need_new_game
    need_new_game = False
    global girl_number
    girl_number = 10
    girl = random.sample(range(81), girl_number)
    global girl_coordinates
    girl_coordinates = list(map(lambda m: divmod(m, 9), girl))
    global girl_map
    girl_map = [[True] * 9 for i in range(9)]
    for i in range(9):
        for j in range(9):
            rect(i*60-270, j*60-210, 60, 'gray')
    rect(4*60-270, 10*60-210, 60, 'yellow')

new_game()
turtle.onscreenclick(click)
turtle.done()