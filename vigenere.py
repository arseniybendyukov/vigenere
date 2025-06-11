from typing import List


# Der Koinzidenzindex (KI) wird oft in der Kryptographie angewendet,
# um verschlüsselte oder unverständliche Texte auf sprachliche Eigenschaften zu untersuchen.
# Der KI ist die Wahrscheinlichkeit, dass zwei zufällig aus dem Text gewählte Symbole gleich sind.
KI = 0.078 # Der Koinzidenzindex für deutschsprachige Texte


# Ä = AE, Ü = UE, Ö = OE, ẞ = SS
BUCHSTABEN_HAEUFIGKEITEN = {
    "E": 0.1741,
    "N": 0.0978,
    "I": 0.0755,
    "S": 0.0789,
    "R": 0.0700,
    "A": 0.0651, 
    "T": 0.0615,
    "D": 0.0508,
    "H": 0.0476,
    "U": 0.0435,
    "L": 0.0344,
    "C": 0.0306,
    "G": 0.0301,
    "M": 0.0253,
    "O": 0.0251,
    "B": 0.0189,
    "W": 0.0189,
    "F": 0.0166,
    "K": 0.0121,
    "Z": 0.0113,
    "P": 0.0079,
    "V": 0.0067,
    "J": 0.0027,
    "Y": 0.0004,
    "X": 0.0003,
    "Q": 0.0002
}


ALPHABET = ''.join(sorted(BUCHSTABEN_HAEUFIGKEITEN.keys()))
VIGENERE_TABELLE = None


def vigenere_tabelle_fuellen():
    '''
        Füllt die globale Variable `VIGENERE_TABELLE`
    '''
    global VIGENERE_TABELLE
    VIGENERE_TABELLE = []
    for i in range(len(ALPHABET)):
        VIGENERE_TABELLE.append([*ALPHABET[i:], *ALPHABET[:i]])


def text_normalisieren(text: str) -> str:
    '''
        Gibt den Text aus, der nur aus in `ALPHABET` enthaltenen Symbolen besteht.
    '''
    return ''.join([symbol.upper() if symbol.upper() in ALPHABET else '' for symbol in text])


def symbol_verschluesseln(text_symbol: str, passwort_symbol: str) -> str:
    '''
        Gibt nach Vigenere verschlüsseltes Symbol aus.
        `text_symbol` und `passwort_symbol` müssen in `ALPHABET` enthalten sein.
    '''
    if text_symbol.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {text_symbol}')
    if passwort_symbol.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {passwort_symbol}')
    i1 = ALPHABET.index(text_symbol.upper())
    i2 = ALPHABET.index(passwort_symbol.upper())
    verschluesselt_symbol = VIGENERE_TABELLE[i1][i2]
    return verschluesselt_symbol if text_symbol.isupper() else verschluesselt_symbol.lower()


def symbol_entschluesseln(verschluesselt_symbol: str, passwort_symbol: str) -> str:
    '''
        Gibt nach Vigenere entschlüsseltes Symbol aus.
        `verschluesselt_symbol` und `passwort_symbol` müssen in `ALPHABET` enthalten sein.
    '''
    if verschluesselt_symbol.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {verschluesselt_symbol}')
    if passwort_symbol.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {passwort_symbol}')
    i1 = ALPHABET.index(passwort_symbol.upper())
    i2 = VIGENERE_TABELLE[i1].index(verschluesselt_symbol.upper())
    text_symbol = ALPHABET[i2]
    return text_symbol if verschluesselt_symbol.isupper() else text_symbol.lower()


def text_verschluesseln(text: str, passwort: str) -> str:
    '''
        Gibt nach Vigenere verschlüsselten Text aus. Die in `ALPHABET` nicht enthaltene Symbole werden 'übersprungen'.
    '''
    verschluesselt = [*text]
    nicht_alphabetisch_symbole_anzahl = 0
    for i in range(len(text)):
        symbol = text[i]
        if symbol.upper() in ALPHABET:
            symbol = symbol_verschluesseln(
                symbol,
                passwort[(i - nicht_alphabetisch_symbole_anzahl) % len(passwort)],
            )
        else:
            nicht_alphabetisch_symbole_anzahl += 1
        verschluesselt[i] = symbol
    return ''.join(verschluesselt)


def ki_berechnen(text: str) -> int:
    '''
        Gibt den Koinzidenzindex aus.
        Der Koinzidenzindex ist die Summe von Wahrscheinlichkeiten, dass die zwei zufällig aus dem Text gewählten Symbole gleich sind.
        Funktioniert nur mit dem Text, der aus den in `ALPHABET` enthaltenen Symbolen besteht.
    '''
    buchstaben_vorkommen = {buchstabe: 0 for buchstabe in ALPHABET}
    for i in range(len(text)):
        symbol = text[i]
        if symbol.upper() not in ALPHABET:
            raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {symbol}')
        buchstaben_vorkommen[symbol.upper()] += 1
    buchstaben_anzahl = sum(buchstaben_vorkommen.values())
    return sum([((vorkommen*(vorkommen-1)) / (buchstaben_anzahl*(buchstaben_anzahl-1))) for vorkommen in buchstaben_vorkommen.values()])
    

def durchschn_ki_berechnen(text: str, passwort_laenge) -> int:
    '''
        Gibt den durchschnittlichen Koinzidenzindex von `passwort_laenge` Symbolgruppen aus.
        Funktioniert nur mit dem Text, der aus den in `ALPHABET` enthaltenen Symbolen besteht.
    '''
    return sum([ki_berechnen(text[i::passwort_laenge]) for i in range(passwort_laenge)]) / passwort_laenge


def beste_passwort_laengen(text: str) -> List[int]:
    '''
        Gibt die nach der Abweichung von `KI` sortierte Liste der Längen der Passwörter aus.
        Die Länge des Passworts muss mindestens 100 Mal kürzer als die Länge des Textes sein (`1 <= len(passwort) <= len(text)/100`).
    '''
    text = text_normalisieren(text)
    passwort_laengen = []
    for passwort_laenge in range(1, int(len(text) / 100)):
        passwort_laengen.append({
            'passwort_laenge': passwort_laenge,
            'ki_abweichung': abs(KI - durchschn_ki_berechnen(text, passwort_laenge)),
        })
    return list(map(
        lambda x: x['passwort_laenge'],
        sorted(passwort_laengen, key=lambda x: x['ki_abweichung'])
    ))


def caesar_verschiebung_ausrechnen(text: str) -> str:
    '''
        Gibt die Verschiebung des nach Caesar verschlüsselten Textes mithilfe des Chi-Quadrat-Tests aus.
        Funktioniert nur mit dem Text, der aus den in `ALPHABET` enthaltenen Symbolen besteht.
    '''
    buchstaben_vorkommen = [0]*len(ALPHABET)
    for i in range(len(text)):
        symbol = text[i]
        if symbol.upper() not in ALPHABET:
            raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {symbol}')
        buchstaben_vorkommen[ALPHABET.index(symbol.upper())] += 1
    buchstaben_anzahl = len(text)
    erwartet = [buchstaben_anzahl * BUCHSTABEN_HAEUFIGKEITEN[s] for s in ALPHABET]
    abweichungen = []
    for caesar_verschiebung in range(len(ALPHABET)):
        abweichung = 0
        for i in range(len(ALPHABET)):
            abweichung += ((erwartet[i] - buchstaben_vorkommen[(i + caesar_verschiebung) % len(ALPHABET)]) ** 2) / erwartet[i]
        abweichungen.append(abweichung)
    return ALPHABET[abweichungen.index(min(abweichungen))]


def passwort_ausrechnen(text: str, password_length: int) -> str:
    '''
        Gibt den Schlüssel für den nach Vigenere verschlüsselten Text aus.
        Funktioniert nur mit dem Text, der aus den in `ALPHABET` enthaltenen Symbolen besteht.
    '''
    text = text_normalisieren(text)
    return ''.join([caesar_verschiebung_ausrechnen(text[i::password_length]) for i in range(password_length)])


def text_entschluesseln(text: str, passwort: str) -> str:
    '''
        Entschlüsselt den nach Vigenere verschlüsselten Text.
    '''
    entschluesselt = [*text]
    nicht_alphabetisch_symbole_anzahl = 0
    for i in range(len(text)):
        symbol = text[i]
        if symbol.upper() in ALPHABET:
            symbol = symbol_entschluesseln(
                symbol,
                passwort[(i - nicht_alphabetisch_symbole_anzahl) % len(passwort)],
            )
        else:
            nicht_alphabetisch_symbole_anzahl += 1
        entschluesselt[i] = symbol
    return ''.join(entschluesselt)
