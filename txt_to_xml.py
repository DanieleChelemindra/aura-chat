import curses
import subprocess
import sys
import os
import xml.etree.ElementTree as ET

#logica di business

def convert_single_file(txt_file, xml_file):
    if not os.path.exists(txt_file):
        return False
    
    try:
        with open(txt_file, "r", encoding="utf-8") as f_in:
            righe = f_in.readlines()

        with open(xml_file, "w", encoding="utf-8") as f_out:
            # Intestazione XML manuale
            f_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f_out.write('<logs>\n')

            for riga in righe:
                riga = riga.strip()
                if not riga: continue

                # Parsing manuale della riga: [YYYY-MM-DD HH:MM:SS] MESSAGGIO
                # Cerchiamo di separare il timestamp dal resto
                if riga.startswith("[") and "]" in riga:
                    parti = riga.split("] ", 1)
                    timestamp = parti[0].replace("[", "")
                    contenuto = parti[1] if len(parti) > 1 else ""
                else:
                    timestamp = "N/A"
                    contenuto = riga

                # Determiniamo il Level e la Source in base alle parole chiave nei tuoi file
                # (Dati derivati dalle stringhe fisse in Server.py e Client.py)
                level = "INFO"
                source = "Sistema"
                
                if "RICEVUTO" in contenuto:
                    level = "IN"
                elif "INVIATO" in contenuto:
                    level = "OUT"
                elif "CONNESSO" in contenuto:
                    level = "CONN"

                if "client_log" in txt_file:
                    source = "Client"
                elif "server_log" in txt_file:
                    source = "Server"

                # Scrittura manuale del tag entry in formato asciutto
                f_out.write(f'  <entry>\n')
                f_out.write(f'    <timestamp>{timestamp}</timestamp>\n')
                f_out.write(f'    <level>{level}</level>\n')
                f_out.write(f'    <source>{source}</source>\n')
                f_out.write(f'    <message>{contenuto}</message>\n')
                f_out.write(f'  </entry>\n')

            f_out.write('</logs>')
        return True
    except Exception as e:
        return False

def esegui_conversione(stdscr):
    """Esegue la conversione dei log client e server."""
    res_client = convert_single_file("client_log.txt", "client_log.xml")
    res_server = convert_single_file("server_log.txt", "server_log.xml")
    
    h, w = stdscr.getmaxyx()
    msg = "Conversione completata!" if (res_client or res_server) else "Nessun file .txt trovato."
    stdscr.addstr(h-2, w//2 - len(msg)//2, msg, curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch() # Attende un tasto

def esegui_cancellazione(stdscr):
    """Cancella i file di log (.txt e .xml)."""
    files_to_delete = [
        "client_log.txt", "server_log.txt",
        "client_log.xml", "server_log.xml"
    ]
    
    deleted_count = 0
    for f in files_to_delete:
        if os.path.exists(f):
            try:
                os.remove(f)
                deleted_count += 1
            except:
                pass

    h, w = stdscr.getmaxyx()
    msg = f"Cancellati {deleted_count} file di log."
    stdscr.addstr(h-2, w//2 - len(msg)//2, msg, curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch() # Attende un tasto


#CURSES

def menu_logs(stdscr):
    curses.curs_set(0)

    voci = [
        "Converti XML",
        "Cancella log",
        "Torna indietro"
    ]

    selezionata = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Titolo
        titolo = "GESTIONE LOG & XML"
        stdscr.addstr(h // 2 - len(voci) // 2 - 3, w // 2 - len(titolo) // 2, titolo)

        # Disegna il menu
        for i, voce in enumerate(voci):
            x = w // 2 - len(voce) // 2
            y = h // 2 - len(voci) // 2 + i

            if i == selezionata:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, voce)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, voce)

        # Input utente
        key = stdscr.getch()

        if key == curses.KEY_UP and selezionata > 0:
            selezionata -= 1

        elif key == curses.KEY_DOWN and selezionata < len(voci) - 1:
            selezionata += 1

        elif key in [10, 13]:  # INVIO
            scelta = voci[selezionata]

            if scelta == "Converti XML":
                esegui_conversione(stdscr)

            elif scelta == "Cancella log":
                esegui_cancellazione(stdscr)

            elif scelta == "Torna indietro":
                curses.endwin()
                subprocess.run([sys.executable, "main.py"])
                break

        stdscr.refresh()

def main():
    curses.wrapper(menu_logs)

if __name__ == "__main__":
    main()