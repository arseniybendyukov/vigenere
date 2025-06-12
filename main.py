from terminal import (
  benutzer_begruessen,
  input_dateiname_anfragen,
  output_dateiname_anfragen,
  fragen_ob_entschluesselt,
  entschluesselt_text_anzeigen,
  erfolgreiche_entschlüsselung_anzeigen,
  sich_entschuldigen,
)
from vigenere import (
  vigenere_tabelle_fuellen,
  beste_passwort_laengen,
  passwort_ausrechnen,
  text_entschluesseln,
)


# Der Name der Datei, in die der entschlüsselte Text gespeichert wird 
DEFAULT_ENTSCHLUESSELT_DATEINAME = 'entschluesselt.txt'


def main():
  vigenere_tabelle_fuellen()

  benutzer_begruessen()

  try:
    input_dateiname = input_dateiname_anfragen()
  except:
    return
  
  with open(input_dateiname, 'r') as verschluesselt_datei:
    verschluesselt_text = verschluesselt_datei.read()

    for passwort_laenge in beste_passwort_laengen(verschluesselt_text):
      passwort = passwort_ausrechnen(verschluesselt_text, passwort_laenge)
      entschluesselt_text = text_entschluesseln(verschluesselt_text, passwort)
      entschluesselt_text_anzeigen(entschluesselt_text)

      antwort = fragen_ob_entschluesselt()

      if antwort:
        try:
          output_dateiname = output_dateiname_anfragen(DEFAULT_ENTSCHLUESSELT_DATEINAME)
        except:
          return
        with open(output_dateiname, 'w') as entschluesselt_datei:
          entschluesselt_datei.writelines(entschluesselt_text)
        erfolgreiche_entschlüsselung_anzeigen(passwort, output_dateiname)
        break
    else:
      sich_entschuldigen()


if __name__ == '__main__':
  main()
