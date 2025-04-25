from string import ascii_uppercase


ALPHABET = ascii_uppercase
MATRIX = None


def fill_vigenere_matrix():
    global MATRIX
    MATRIX = []
    for i in range(len(ALPHABET)):
        MATRIX.append([*ALPHABET[i:], *ALPHABET[:i]])
       
       
fill_vigenere_matrix()
        
print(MATRIX)


def encode_symbol_vigenere(s1, s2):
    pass


s1 = ''
s2 = ''
print(encode_symbol_vigenere(s1, s2))
