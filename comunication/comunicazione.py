import curses
import subprocess
import sys
import os

def apri_nuovo_terminale(nomeScript):
    comando = f'''
    tell application "Terminal"
        do script "cd '{os.getcwd()}' && python3 {nomeScript}"
        activate
    end tell
    '''
    subprocess.Popen(["osascript", "-e", comando])

def comunicazione(stdscr):
    curses.curs_set(0)

    voci = [
        "server",
        "client",
        "torna indietro"
    ]

    selezionata = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        titolo = "MENÙ COMUNICAZIONE"
        stdscr.addstr(h // 2 - len(voci) // 2 - 2,
                      w // 2 - len(titolo) // 2,
                      titolo)

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

        elif key in [10, 13]:  # INVIO
            scelta = voci[selezionata]

            if scelta == "torna indietro":
                curses.endwin()
                subprocess.run([sys.executable, "main.py"])
                return

            elif scelta == "server":
                apri_nuovo_terminale("server.py")

            elif scelta == "client":
                apri_nuovo_terminale("client.py")


        stdscr.refresh()


def main():
    curses.wrapper(comunicazione)


if __name__ == "__main__":
    main()
