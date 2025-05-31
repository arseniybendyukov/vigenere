import os
from ui import greetings,\
               get_filename,\
               ask_if_decoded,\
               apologize,\
               success,\
               background
from logic import fill_vigenere_matrix,\
                  get_best_key_lengths,\
                  decode_text_vigenere,\
                  get_vigenere_password,\
                  get_trimmed_text


DECODED_TEXT_FILENAME = 'entschluesselt.txt'


def main():
  fill_vigenere_matrix()

  greetings()

  try:
    filename = get_filename()
  except:
    return
  
  with open(filename, 'r') as encoded_file:
    encoded_text = encoded_file.read()

    for password_length in get_best_key_lengths(encoded_text):
      password = get_vigenere_password(encoded_text, password_length)
      decoded_text = decode_text_vigenere(encoded_text, password)
      print(background(get_trimmed_text(decoded_text))) 

      answer = ask_if_decoded()

      if answer:
        # Speichert den entschlüsselten Text in 'entschluesselt.txt' im aktuellen Ordner
        with open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), DECODED_TEXT_FILENAME), 'w') as decoded_file:
          decoded_file.writelines(decoded_text)
        success(DECODED_TEXT_FILENAME, password)
        break
    else:
      apologize()


if __name__ == '__main__':
  main()
