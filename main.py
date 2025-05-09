# Ä = AE, Ü = UE, Ö = OE
LETTERS_FREQUENCIES = {
    "E": 0.1740,
    "N": 0.0978,
    "I": 0.0755,
    "S": 0.0727,
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
    "ẞ": 0.0031,
    "J": 0.0027,
    "Y": 0.0004,
    "X": 0.0003,
    "Q": 0.0002
}


ALPHABET = 'ABCDEFGHIKLMNOPQRSTUVWXYZẞ'
MATRIX = None


def fill_vigenere_matrix():
    '''
        Füllt die globale Variable MATRIX (Vigenere-Tabelle)
    '''
    global MATRIX
    MATRIX = []
    for i in range(len(ALPHABET)):
        MATRIX.append([*ALPHABET[i:], *ALPHABET[:i]])


def encode_symbol_vigenere(s1: str, s2: str) -> str:
    '''
        Gibt nach Vigenere verschlüsseltes Symbol aus (Großgeschrieben).
    '''
    if s1.upper() not in ALPHABET or s2.upper() not in ALPHABET:
        raise VelueError('Es gibt einen Buchstaben, der nicht im ALPHABET enthalten!')
    i1 = ALPHABET.index(s1.upper())
    i2 = ALPHABET.index(s2.upper())
    return MATRIX[i1][i2]


def encode_text_vigenere(text: str, password: str) -> str:
    '''
        Gibt nach Vigenere verschlüsselten Text aus. Die im ALPHABET nicht enthaltene Symbole werden 'übersprungen'.
    '''
    encoded = [*text]
    non_alphabetic_symbols_count = 0
    for i in range(len(text)):
        symbol = text[i]
        if symbol.upper() in ALPHABET:
            symbol = encode_symbol_vigenere(
                symbol,
                password[(i - non_alphabetic_symbols_count) % len(password)],
            )
        else:
            non_alphabetic_symbols_count += 1
        encoded[i] = symbol
    return ''.join(encoded)


def find_password_length(text: str):
    pass


if __name__ == '__main__':
    fill_vigenere_matrix()
    text = 'Das Leben in der Stadt und auf dem Land unterscheidet sich in vielen Aspekten. In der Stadt gibt es meist mehr Moeglichkeiten: Arbeitsplaetze, Bildungseinrichtungen, kulturelle Angebote und eine bessere Infrastruktur. Viele Menschen schaetzen das Stadtleben wegen seiner Vielfalt und dem schnellen Zugang zu allem, was man im Alltag braucht. Gleichzeitig kann es in der Stadt auch stressig, laut und ueberfuellt sein. Auf dem Land hingegen ist das Leben ruhiger. Die Menschen kennen sich oft untereinander, und die Natur ist meist direkt vor der Haustuer. Besonders Familien mit Kindern oder aeltere Menschen ziehen gerne aufs Land, weil es dort weniger Verkehr, mehr Platz und eine engere Gemeinschaft gibt. Allerdings kann es schwieriger sein, ohne Auto mobil zu bleiben, und viele Dienstleistungen oder Einkaufmoeglichkeiten sind weiter entfernt. Beide Lebensformen haben ihre Vor- und Nachteile. Letztlich haengt die Entscheidung, wo man leben moechte, stark von den persoenlichen Beduerfnissen und Prioritaeten ab. Waehrend manche das pulsierende Leben der Stadt lieben, bevorzugen andere die Ruhe und Naturverbundenheit des Landlebens. Eine ideale Loesung koennte auch eine Mischung aus beidem sein – zum Beispiel in einer kleineren Stadt oder einem gut angebundenen Vorort.'
    password = 'ABCD'
    encoded_text = encode_text_vigenere(text, password)
    print(encoded_text)
