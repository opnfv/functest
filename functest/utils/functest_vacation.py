from os import environ
from curses import initscr, curs_set, newwin, endwin,\
    KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from random import randrange


def main():
    environ["TERM"] = 'Eterm'
    initscr()
    curs_set(0)
    try:
        win = newwin(16, 60, 0, 0)
        win.keypad(True)
        win.nodelay(True)
        win.border('|', '|', '-', '-', '+', '+', '+', '+')
        win.addch(4, 44, '@')
        win.addstr(0, 5, ' Eat all the OPNFV bugs by FunTest! ')
        win.addstr(15, 7, ' Left,Right,Up,Down: move; other keys: quit ')
        snake = [[20, 7], [19, 7], [18, 7], [17, 7],
                 [16, 7], [15, 7], [14, 7], [13, 7]]
        key = KEY_RIGHT
        body = '~FUNTEST'
        ind = 0
        while key != 27:
            win.addstr(0, 44, ' Score: '+str(len(snake)-len(body))+' ')
            win.timeout(140 - 2 * len(snake))
            getkey = win.getch()
            key = key if getkey == -1 else getkey
            snake.insert(
                0, [snake[0][0]+(key == KEY_RIGHT and 1 or
                                 key == KEY_LEFT and -1),
                    snake[0][1]+(key == KEY_DOWN and 1 or
                                 key == KEY_UP and -1)])
            win.addch(snake[len(snake)-1][1], snake[len(snake)-1][0], ' ')
            if win.inch(snake[0][1], snake[0][0]) & 255 == 32:
                snake.pop()
            elif win.inch(snake[0][1], snake[0][0]) & 255 == ord('@'):
                c = [n for n in [[randrange(1, 58, 1), randrange(1, 14, 1)]
                     for x in range(len(snake))] if n not in snake]
                win.addch(c == [] and 4 or c[0][1],
                          c == [] and 44 or c[0][0], '@')
            else:
                break
            ind += 1
            win.addch(snake[0][1], snake[0][0], body[ind % len(body)])
    finally:
        endwin()

    print '\nSnake.PY-26lines by Kris Cieslak (defaultset.blogspot.com).'
    print 'OPNFV adaptation by Functest dream team.'
    print 'Thanks for playing, your score: '+str(len(snake)-len(body)-1)+'.'
    print 'Find and fix more bugs in your real OPNFV setup!\n'
