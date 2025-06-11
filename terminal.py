import os
import tkinter
from tkinter import filedialog


class ANSI:
  TITEL = '\033[96m'
  HINTERGRUND = '\033[47m'
  GRUEN = '\033[92m'
  GELB = '\033[93m'
  ROT = '\033[91m'
  UNTERSTRICH = '\033[4m'
  ENDE = '\033[0m'


def titel(text: str) -> str:
  return f'{ANSI.TITEL}{text}{ANSI.ENDE}'


def hintergrund(text: str) -> str:
  return f'{ANSI.HINTERGRUND}{text}{ANSI.ENDE}'


def gruen(text: str) -> str:
  return f'{ANSI.GRUEN}{text}{ANSI.ENDE}'


def gelb(text: str) -> str:
  return f'{ANSI.GELB}{text}{ANSI.ENDE}'


def rot(text: str) -> str:
  return f'{ANSI.ROT}{text}{ANSI.ENDE}'


def unterstrich(text: str) -> str:
  return f'{ANSI.UNTERSTRICH}{text}{ANSI.ENDE}'


def ja_oder_nein_unterbrechen(platzhalter: str):
  while True:
    antwort = input(f'{platzhalter} j/n: ')
    if antwort == 'j':
      return
    if antwort == 'n':
      raise KeyboardInterrupt
    print(rot('Bitte geben Sie entweder \'j\' oder \'n\' ein.'))


def benutzer_begruessen():
  print(titel('Hallo! Bitte wählen Sie eine Text-Datei, die Sie entschlüsseln wollen.'))


def fragen_ob_entschluesselt() -> bool:
  antwort = input(f'{unterstrich('Sieht dieser Text wie ein deutscher Klartext aus?')} j/n: ')

  while True:  
    if antwort == 'j':
      return True
    elif antwort == 'n':
      return False
    else:
      antwort = input(rot('Bitte geben Sie entweder \'j\' oder \'n\' ein: '))


def dateiname_anfragen() -> str:
  '''
    Öffnet den Explorer, sodass der Benutzer eine Textdatei auswählen kann.
    Gibt den Dateinamen aus.
  '''
  window = tkinter.Tk() # Initialisierung des Moduls
  window.wm_attributes('-topmost', 1) # damit das Fenster immer oben bleibt
  window.withdraw() # damit das Fenster beim Initialisieren nicht geöffnet wird

  dateiname =  filedialog.askopenfilename(filetypes=[('Text-Datei', '*.txt',)])
  if dateiname != '':
    return dateiname
  ja_oder_nein_unterbrechen(f'{rot('Sie haben nichts gewählt.')} Wollen Sie noch einmal versuchen?')
  return dateiname_anfragen()


def entschluesselt_dateipfad(dateiname: str) -> str:
  '''
    Gibt den absoluten Pfad der Datei mit dem Namen `dateiname` im aktuellen Ordner.
  '''
  return os.path.join(
    os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))),
    dateiname
  )


def text_kürzen(text: str) -> str:
    '''
        Gibt die ersten 80 Symbolen aus dem Text aus.
    '''
    return text[:80] + '...' if len(text) > 80 else text


def entschluesselt_text_anzeigen(decoded_text: str):
  print(hintergrund(text_kürzen(decoded_text)))


def erfolgreiche_entschlüsselung_anzeigen(passwort: str, dateiname: str):
  print(f'Prima! Passwort: \'{gruen(passwort)}\'. Der entschlüsselte Text wurde in \'{unterstrich(dateiname)}\' gespeichert.')


def sich_entschuldigen():
  print(gelb('Entschuldigung. Das Programm kann diesen Text leider nicht knacken :('))
