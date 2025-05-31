from typing import List


# Der Koinzidenzindex für deutschsprachige Texte
IC = 0.078


# Ä = AE, Ü = UE, Ö = OE, ẞ = SS
LETTERS_FREQUENCIES = {
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


ALPHABET = ''.join(sorted(LETTERS_FREQUENCIES.keys()))
MATRIX = None


def fill_vigenere_matrix():
    '''
        Füllt die globale Variable `MATRIX` (Vigenere-Tabelle)
    '''
    global MATRIX
    MATRIX = []
    for i in range(len(ALPHABET)):
        MATRIX.append([*ALPHABET[i:], *ALPHABET[:i]])


def get_clear_text(text: str) -> str:
    '''
        Gibt den Text aus, der nur aus in `ALPHABET` enthaltenen Symbolen besteht.
    '''
    return ''.join([symbol.upper() if symbol.upper() in ALPHABET else '' for symbol in text])


def encode_symbol_vigenere(text_symbol: str, password_symbol: str) -> str:
    '''
        Gibt nach Vigenere verschlüsseltes Symbol aus.
    '''
    if text_symbol.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {text_symbol}')
    if password_symbol.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {password_symbol}')
    i1 = ALPHABET.index(text_symbol.upper())
    i2 = ALPHABET.index(password_symbol.upper())
    text_symbol_encoded = MATRIX[i1][i2]
    return text_symbol_encoded if text_symbol.isupper() else text_symbol_encoded.lower()


def decode_symbol_vigenere(cipher_symbol: str, password_symbol: str) -> str:
    '''
        Gibt nach Vigenere entschlüsseltes Symbol aus.
    '''
    if cipher_symbol.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {cipher_symbol}')
    if password_symbol.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {password_symbol}')
    i1 = ALPHABET.index(password_symbol.upper())
    i2 = MATRIX[i1].index(cipher_symbol.upper())
    decoded_symbol = ALPHABET[i2]
    return decoded_symbol if cipher_symbol.isupper() else decoded_symbol.lower()


def encode_text_vigenere(text: str, password: str) -> str:
    '''
        Gibt nach Vigenere verschlüsselten Text aus. Die in `ALPHABET` nicht enthaltene Symbole werden 'übersprungen'.
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


def get_ic(text: str) -> int:
    '''
        Gibt den Koinzidenzindex aus.
        Der Koinzidenzindex ist die Summe von Wahrscheinlichkeiten,
        dass die zwei zufällig aus dem Text gewählten Symbole gleich sind.
        Funktioniert nur mit dem Text, der aus den in `ALPHABET` enthaltenen Symbolen besteht.
    '''
    occurences = {letter: 0 for letter in ALPHABET}
    for i in range(len(text)):
        symbol = text[i]
        if symbol.upper() not in ALPHABET:
            raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {symbol}')
        occurences[symbol.upper()] += 1
    letters_count = sum(occurences.values())
    return sum([((frequency*(frequency-1)) / (letters_count*(letters_count-1))) for frequency in occurences.values()])
    

def get_avg_ic(text: str, password_length) -> int:
    '''
        Gibt den durchschnittlichen Koinzidenzindex von `password_length` Symbolgruppen aus.
        Funktioniert nur mit dem Text, der aus den in `ALPHABET` enthaltenen Symbolen besteht.
    '''
    return sum([get_ic(text[i::password_length]) for i in range(password_length)]) / password_length


def get_best_key_lengths(text: str) -> List[int]:
    '''
        Gibt die nach der Abweichung von IC sortierte Liste der Längen der Passwörter aus.
        Die Länge des Passworts muss mindestens 100 Mal kürzer als die Länge des Textes sein (`1 <= len(password) <= len(text)/100`).
    '''
    text = get_clear_text(text)
    password_lengths = []
    for password_length in range(1, int(len(text) / 100)):
        password_lengths.append({
            'password_length': password_length,
            'ic_difference': abs(IC - get_avg_ic(text, password_length)),
        })
    return map(lambda x: x['password_length'], sorted(password_lengths, key=lambda x: x['ic_difference']))


def get_caesar_shift(text: str) -> str:
    '''
        Gibt die Verschiebung des nach Caesar verschlüsselten Textes mithilfe des Chi-Quadrat-Tests aus.
    '''
    occurences = [0]*len(ALPHABET)
    for i in range(len(text)):
        symbol = text[i]
        if symbol.upper() not in ALPHABET:
            raise ValueError(f'Es gibt ein Symbol, der nicht in ALPHABET enthalten ist: {symbol}')
        occurences[ALPHABET.index(symbol.upper())] += 1
    letters_count = len(text)
    expected = [letters_count * LETTERS_FREQUENCIES[s] for s in ALPHABET]
    errors = []
    for shift in range(len(ALPHABET)):
        error = 0
        for i in range(len(ALPHABET)):
            error += ((expected[i] - occurences[(i + shift) % len(ALPHABET)]) ** 2) / expected[i]
        errors.append(error)
    return ALPHABET[errors.index(min(errors))]


def get_vigenere_password(text: str, password_length: int) -> str:
    '''
        Gibt den Schlüssel für den nach Vigenere verschlüsselten Text aus.
        Funktioniert nur mit dem Text, der aus den in `ALPHABET` enthaltenen Symbolen besteht.
    '''
    text = get_clear_text(text)
    return ''.join([get_caesar_shift(text[i::password_length]) for i in range(password_length)])


def decode_text_vigenere(text: str, password: str) -> str:
    '''
        Entschlüsselt den nach Vigenere verschlüsselten Text.
    '''
    decoded = [*text]
    non_alphabetic_symbols_count = 0
    for i in range(len(text)):
        symbol = text[i]
        if symbol.upper() in ALPHABET:
            symbol = decode_symbol_vigenere(
                symbol,
                password[(i - non_alphabetic_symbols_count) % len(password)],
            )
        else:
            non_alphabetic_symbols_count += 1
        decoded[i] = symbol
    return ''.join(decoded)


def get_trimmed_text(text: str) -> str:
    '''
        Gibt die ersten 80 Symbolen aus dem Text aus.
    '''
    return text[:80] + '...' if len(text) > 80 else text
