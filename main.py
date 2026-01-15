import curses
import subprocess
import sys

def menu(stdscr):
    curses.curs_set(0)

    voci = [
        "comunicazione",
        "registrati",
        "log",
        "Esci"
    ]

    selezionata = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        titolo = " aura chat "
        stdscr.addstr(h // 2 - len(voci) // 2 - 3, w // 2 - len(titolo) // 2, titolo, curses.A_REVERSE)


        for i, voce in enumerate(voci):
            x = w // 2 - len(voce) // 2
            y = h // 2 - len(voci) // 2 + i

            if i == selezionata:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, voce)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, voce)

        key = stdscr.getch()

        if key == curses.KEY_UP and selezionata > 0:
            selezionata -= 1
        elif key == curses.KEY_DOWN and selezionata < len(voci) - 1:
            selezionata += 1
        elif key in [10, 13]:
            scelta = voci[selezionata]

            if scelta == "Esci":
                break

            elif scelta == "registrati":
                curses.endwin()
                subprocess.run([sys.executable, "login/login.py"])
                break

            elif scelta == "comunicazione":
                curses.endwin()
                subprocess.run([sys.executable, "comunication/comunicazione.py"])
                break

            elif scelta == "log":
                curses.endwin()
                subprocess.run([sys.executable, "txt_to_xml.py"])
                break

        stdscr.refresh()

curses.wrapper(menu)
