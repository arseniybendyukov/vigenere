from terminal import (
  benutzer_begruessen,
  dateiname_anfragen,
  fragen_ob_entschluesselt,
  entschluesselt_dateipfad,
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
ENTSCHLUESSELT_DATEINAME = 'entschluesselt.txt'


def main():
  vigenere_tabelle_fuellen()

  benutzer_begruessen()

  try:
    dateiname = dateiname_anfragen()
  except:
    return
  
  with open(dateiname, 'r') as verschluesselt_datei:
    verschluesselt_text = verschluesselt_datei.read()

    for passwort_laenge in beste_passwort_laengen(verschluesselt_text):
      passwort = passwort_ausrechnen(verschluesselt_text, passwort_laenge)
      entschluesselt_text = text_entschluesseln(verschluesselt_text, passwort)
      entschluesselt_text_anzeigen(entschluesselt_text)

      antwort = fragen_ob_entschluesselt()

      if antwort:
        # Speichert den entschlüsselten Text in eine Datei im aktuellen Ordner
        with open(entschluesselt_dateipfad(ENTSCHLUESSELT_DATEINAME), 'w') as entschluesselt_datei:
          entschluesselt_datei.writelines(entschluesselt_text)
        erfolgreiche_entschlüsselung_anzeigen(passwort, ENTSCHLUESSELT_DATEINAME)
        break
    else:
      sich_entschuldigen()


if __name__ == '__main__':
  main()
