import tkinter
from tkinter import filedialog


class ANSI_CODES:
  HEADER = '\033[96m'
  BACKGROUND = '\033[47m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  UNDERLINE = '\033[4m'
  ENDC = '\033[0m'


def header(text: str) -> str:
  return f'{ANSI_CODES.HEADER}{text}{ANSI_CODES.ENDC}'


def background(text: str) -> str:
  return f'{ANSI_CODES.BACKGROUND}{text}{ANSI_CODES.ENDC}'


def green(text: str) -> str:
  return f'{ANSI_CODES.GREEN}{text}{ANSI_CODES.ENDC}'


def purple(text: str) -> str:
  return f'{ANSI_CODES.YELLOW}{text}{ANSI_CODES.ENDC}'


def red(text: str) -> str:
  return f'{ANSI_CODES.RED}{text}{ANSI_CODES.ENDC}'


def underline(text: str) -> str:
  return f'{ANSI_CODES.UNDERLINE}{text}{ANSI_CODES.ENDC}'


def yes_or_no_interrupt(placeholder: str):
  while True:
    answer = input(f'{placeholder} j/n: ')
    if answer == 'j':
      return
    if answer == 'n':
      raise KeyboardInterrupt
    print(red('Bitte geben Sie entweder \'j\' oder \'n\' ein.'))


def greet_user():
  print(header('Hallo! Bitte wählen Sie eine Text-Datei, die Sie entschlüsseln wollen.'))


def show_successfull_decoding(password: str, filename: str):
  print(f'Prima! Passwort: \'{green(password)}\'. Der entschlüsselte Text wurde in \'{underline(filename)}\' gespeichert.')


def apologize():
  print(purple('Entschuldigung. Das Programm kann diesen Text leider nicht knacken :('))


def ask_if_decoded() -> bool:
  answer = input(f'{underline('Sieht dieser Text wie ein deutscher Klartext aus?')} j/n: ')

  while True:  
    if answer == 'j':
      return True
    elif answer == 'n':
      return False
    else:
      answer = input(red('Bitte geben Sie entweder \'j\' oder \'n\' ein: '))


def get_filename() -> str:
  window = tkinter.Tk()
  window.wm_attributes('-topmost', 1)
  window.withdraw()

  filename =  filedialog.askopenfilename(filetypes=[('Text-Datei', '*.txt',)])
  if filename != '':
    return filename
  yes_or_no_interrupt(f'{red('Sie haben nichts gewählt.')} Wollen Sie noch einmal versuchen?')
  return get_filename()


def get_trimmed_text(text: str) -> str:
    '''
        Gibt die ersten 80 Symbolen aus dem Text aus.
    '''
    return text[:80] + '...' if len(text) > 80 else text


def show_decoded_text(decoded_text: str):
  print(background(get_trimmed_text(decoded_text)))
