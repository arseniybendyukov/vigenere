import tkinter
from tkinter import filedialog


class COLORS:
  HEADER = '\033[96m'
  BACKGROUND = '\033[47m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  UNDERLINE = '\033[4m'
  ENDC = '\033[0m'


def header(text: str) -> str:
  return f'{COLORS.HEADER}{text}{COLORS.ENDC}'


def background(text: str) -> str:
  return f'{COLORS.BACKGROUND}{text}{COLORS.ENDC}'


def green(text: str) -> str:
  return f'{COLORS.GREEN}{text}{COLORS.ENDC}'


def purple(text: str) -> str:
  return f'{COLORS.YELLOW}{text}{COLORS.ENDC}'


def red(text: str) -> str:
  return f'{COLORS.RED}{text}{COLORS.ENDC}'


def underline(text: str) -> str:
  return f'{COLORS.UNDERLINE}{text}{COLORS.ENDC}'


def yes_or_no_interrupt(placeholder: str):
  while True:
    answer = input(f'{placeholder} y/n: ')
    if answer == 'y':
      return
    if answer == 'n':
      raise KeyboardInterrupt
    print(red('Bitte geben Sie entweder \'y\' oder \'n\' ein.'))


def greetings():
  print(header('Hallo! Bitte wählen Sie eine Text-Datei, die Sie entschlüsseln wollen.'))


def success(filename: str, password: str):
  print(f'Prima! Passwort: \'{green(password)}\'. Der entschlüsselte Text wurde in \'{underline(filename)}\' gespeichert.')


def apologize():
  print(purple('Entschuldigung. Das Programm kann diesen Text leider nicht knacken :('))


def ask_if_decoded() -> bool:
  answer = input(f'{underline('Sieht dieser Text wie ein deutscher Klartext aus?')} y/n: ')

  while True:  
    if answer == 'y':
      return True
    elif answer == 'n':
      return False
    else:
      answer = input(red('Bitte geben Sie entweder \'y\' oder \'n\' ein: '))


def get_filename() -> str:
  window = tkinter.Tk()
  window.wm_attributes('-topmost', 1)
  window.withdraw()

  filename =  filedialog.askopenfilename(filetypes=[('Text-Datei', '*.txt',)])
  if filename != '':
    return filename
  yes_or_no_interrupt(f'{red('Sie haben nichts gewählt.')} Wollen Sie noch einmal versuchen?')
  return get_filename()
