import curses
import subprocess
import sys

def login_page(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    username = ""
    password = ""
    campo_attivo = 0  # 0=user, 1=pass, 2=accedi, 3=crea, 4=menu

    while True:
        stdscr.clear()

        # ---- TORNA AL MENU ----
        menu_text = "Torna al menù"
        if campo_attivo == 4:
            stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(1, w//2 - len(menu_text)//2, menu_text)
        if campo_attivo == 4:
            stdscr.attroff(curses.A_REVERSE)

        # ---- FORM ----
        stdscr.addstr(4, w//2 - 10, "Nome utente:")
        stdscr.addstr(5, w//2 - 10, "Password:")

        if campo_attivo == 0:
            stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(4, w//2 + 4, username + " ")
        if campo_attivo == 0:
            stdscr.attroff(curses.A_REVERSE)

        if campo_attivo == 1:
            stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(5, w//2 + 4, "*" * len(password) + " ")
        if campo_attivo == 1:
            stdscr.attroff(curses.A_REVERSE)

        # ---- BOTTONI ----
        accedi = "Accedi"
        crea = "Crea account"

        if campo_attivo == 2:
            stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(8, w//2 - len(accedi) - 2, accedi)
        if campo_attivo == 2:
            stdscr.attroff(curses.A_REVERSE)

        if campo_attivo == 3:
            stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(8, w//2 + 2, crea)
        if campo_attivo == 3:
            stdscr.attroff(curses.A_REVERSE)

        stdscr.refresh()
        key = stdscr.getch()

        # ---- NAVIGAZIONE ----
        if key == 9:  # TAB
            campo_attivo = (campo_attivo + 1) % 5

        elif key == curses.KEY_UP:
            campo_attivo = (campo_attivo - 1) % 5

        elif key == curses.KEY_DOWN:
            campo_attivo = (campo_attivo + 1) % 5

        elif key in [10, 13]:  # INVIO
            if campo_attivo == 4:
                curses.endwin()
                subprocess.run([sys.executable, "main.py"])
                return

            elif campo_attivo == 2:
                stdscr.addstr(10, 2, f"Accesso: {username}")
                stdscr.getch()

            elif campo_attivo == 3:
                stdscr.addstr(10, 2, f"Account creato: {username}")
                stdscr.getch()

        # ---- INPUT TESTO ----
        elif campo_attivo == 0 and 32 <= key <= 126:
            username += chr(key)

        elif campo_attivo == 1 and 32 <= key <= 126:
            password += chr(key)

        elif key in (curses.KEY_BACKSPACE, 127):
            if campo_attivo == 0:
                username = username[:-1]
            elif campo_attivo == 1:
                password = password[:-1]


def main():
    curses.wrapper(login_page)


if __name__ == "__main__":
    main()
