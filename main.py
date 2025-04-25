from string import ascii_uppercase


ALPHABET = ascii_uppercase
MATRIX = None


def fill_vigenere_matrix():
    global MATRIX
    MATRIX = []
    for i in range(len(ALPHABET)):
        MATRIX.append([*ALPHABET[i:], *ALPHABET[:i]])


def encode_symbol_vigenere(s1: str, s2: str) -> str:
    '''
        Returns symbol in uppercase.
    '''
    # todo: throw error
    if s1.upper() not in ALPHABET or s2.upper() not in ALPHABET:
        return ''
    i1 = ALPHABET.index(s1.upper())
    i2 = ALPHABET.index(s2.upper())
    return MATRIX[i1][i2]


def encode_text_vigenere(text: str, password: str) -> str:
    encoded = [*text]
    for i in range(len(text)):
        symbol = text[i]
        if symbol.upper() in ALPHABET:
            symbol = encode_symbol_vigenere(
                symbol,
                password[i % len(password)],
            )
        encoded[i] = symbol
    return ''.join(encoded)


if __name__ == '__main__':
    fill_vigenere_matrix()
    text = 'ABCD'
    password = 'C'
    print(encode_text_vigenere(text, password))
