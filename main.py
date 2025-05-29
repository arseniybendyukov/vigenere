from typing import List


# Der Koinzidenzindex für deutschsprachige Texte
IC = 0.078


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


ALPHABET = ''.join(sorted(LETTERS_FREQUENCIES.keys()))
MATRIX = None


def fill_vigenere_matrix():
    '''
        Füllt die globale Variable <MATRIX> (Vigenere-Tabelle)
    '''
    global MATRIX
    MATRIX = []
    for i in range(len(ALPHABET)):
        MATRIX.append([*ALPHABET[i:], *ALPHABET[:i]])


def get_clear_text(text: str) -> str:
    return ''.join([symbol if symbol.upper() in ALPHABET else '' for symbol in text])


def encode_symbol_vigenere(s1: str, s2: str) -> str:
    '''
        Gibt nach Vigenere verschlüsseltes Symbol aus (Großgeschrieben).
    '''
    if s1.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in <ALPHABET> enthalten ist: {s1}')
    if s2.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in <ALPHABET> enthalten ist: {s2}')
    i1 = ALPHABET.index(s1.upper())
    i2 = ALPHABET.index(s2.upper())
    return MATRIX[i1][i2]


def decode_symbol_vigenere(cipher_symbol: str, password_symbol: str) -> str:
    if cipher_symbol.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in <ALPHABET> enthalten ist: {cipher_symbol}')
    if password_symbol.upper() not in ALPHABET:
        raise ValueError(f'Es gibt ein Symbol, der nicht in <ALPHABET> enthalten ist: {password_symbol}')
    i1 = ALPHABET.index(password_symbol.upper())
    i2 = MATRIX[i1].index(cipher_symbol.upper())
    return ALPHABET[i2]


def encode_text_vigenere(text: str, password: str) -> str:
    '''
        Gibt nach Vigenere verschlüsselten Text aus. Die in <ALPHABET> nicht enthaltene Symbole werden 'übersprungen'.
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
        Funktioniert nur mit dem Text, der aus den in <ALPHABET> enthaltenen Symbolen besteht.
    '''
    occurences = {letter: 0 for letter in ALPHABET}
    for i in range(len(text)):
        symbol = text[i]
        if symbol.upper() not in ALPHABET:
            raise ValueError(f'Es gibt ein Symbol, der nicht in <ALPHABET> enthalten ist: {symbol}')
        occurences[symbol.upper()] += 1
    letters_count = sum(occurences.values())
    return sum([((frequency*(frequency-1)) / (letters_count*(letters_count-1))) for frequency in occurences.values()])
    

def get_avg_ic(text: str, password_length) -> int:
    '''
        Gibt den durchschnittlichen Koinzidenzindex von <password_length> Symbolgruppen aus.
        Funktioniert nur mit dem Text, der aus den in <ALPHABET> enthaltenen Symbolen besteht.
    '''
    return sum([get_ic(text[i::password_length]) for i in range(password_length)]) / password_length


def get_best_key_lengths(text: str) -> List[int]:
    '''
        Gibt die nach der Abweichung von IC sortierte Liste der Längen der Passwörter aus.
        Die Länge des Passworts muss mindestens 100 Mal kürzer als die Länge des Textes sein.
        1 <= len(Passwort) <= len(Text)/100
        Funktioniert nur mit dem Text, der aus den in <ALPHABET> enthaltenen Symbolen besteht.
    '''
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
        Funktioniert nur mit dem Text, der aus den in <ALPHABET> enthaltenen Symbolen besteht.
    '''
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


TEXT = 'DER EINFLUSS DER TECHNOLOGIE AUF DIE MODERNE GESELLSCHAFT IN DER HEUTIGEN ZEIT IST TECHNOLOGIE EIN INTEGRALER BESTANDTEIL UNSERES ALLTAGS GEWORDEN. SIE VERAENDERT NICHT NUR, WIE WIR KOMMUNIZIEREN, ARBEITEN UND LERNEN, SONDERN BEEINFLUSST AUCH VIELE GESELLSCHAFTLICHE STRUKTUREN UND LEBENSWEISEN. DER TECHNOLOGISCHE FORTSCHRITT HAT SOWOHL POSITIVE ALS AUCH NEGATIVE AUSWIRKUNGEN, DIE ES WERT SIND, NAEHER BETRACHTET ZU WERDEN. EINE DER SICHTBARSTEN VERAENDERUNGEN DURCH TECHNOLOGIE IST DIE ART UND WEISE, WIE MENSCHEN KOMMUNIZIEREN. DANK SMARTPHONES, SOZIALER MEDIEN UND INSTANT-MESSAGING-DIENSTEN KOENNEN MENSCHEN WELTWEIT IN ECHTZEIT MITEINANDER IN KONTAKT TRETEN. DIESE VERNETZUNG HAT BARRIEREN DER ENTFERNUNG UND ZEIT NAHEZU AUFGEHOBEN UND ERMOEGLICHT ES, FREUNDSCHAFTEN UND ARBEITSBEZIEHUNGEN UEBER GROSSE DISTANZEN AUFRECHTZUERHALTEN. ALLERDINGS BRINGT DIESE DIGITALE KOMMUNIKATION AUCH HERAUSFORDERUNGEN MIT SICH. DIE QUALITAET DER PERSOENLICHEN BEZIEHUNGEN KANN LEIDEN, WENN PERSOENLICHE TREFFEN DURCH VIRTUELLE CHATS ERSETZT WERDEN. ZUDEM ENTSTEHEN NEUE PROBLEME WIE CYBERMOBBING ODER DIE ABHAENGIGKEIT VON DIGITALEN MEDIEN, DIE DAS SOZIALE VERHALTEN BEEINFLUSSEN KOENNEN. TECHNOLOGIE HAT DIE ARBEITSWELT GRUNDDLEGEND VERAENDERT. AUTOMATISIERUNG UND KUENSTLICHE INTELLIGENZ UEBERNEHMEN ZUNEHMEND REPETITIVE AUFGABEN, WAS EINERSEITS DIE PRODUKTIVITAET STEIGERT, ANDERERSEITS ABER AUCH ARBEITSPLAETZE GEFAEHRDET. VIELE BERUFE ERFORDERN HEUTE DIGITALE KOMPETENZEN, UND DIE WEITERBILDUNG WIRD ZUR NOTWENDIGKEIT FUER ARBEITNEHMER. REMOTE-ARBEIT IST EIN WEITERES ERGEBNIS TECHNOLOGISCHER ENTWICKLUNG. INSBESONDERE DURCH DIE COVID-19-PANDEMIE HAT SICH DAS HOMEOFFICE ETABLIERT, WAS FLEXIBILITAET UND EINE BESSERE VEREINBARKEIT VON BERUF UND PRIVATLEBEN ERMOEGLICHT. GLEICHZEITIG STELLT DIESE ARBEITSFORM NEUE ANFORDERUNGEN AN SELBSTDISZIPLIN UND DIGITALE ZUSAMMENARBEIT. AUCH IM BILDUNGSBEREICH HAT TECHNOLOGIE EINEN TIEFGRUENDEN EINFLUSS. DIGITALE LERNPLATTFORMEN UND ONLINE-KURSE MACHEN BILDUNG ZUGAENGLICHER UND FLEXIBLER. SCHUELER UND STUDENTEN KOENNEN UNABHAENGIG VON ORT UND ZEIT LERNEN, WAS INSBESONDERE IN LAENDLICHEN ODER ABGELEGENEN REGIONEN VORTEILE BIETET. DENNOCH GIBT ES AUCH HERAUSFORDERUNGEN, WIE DIE DIGITALE KLUEFT ZWISCHEN VERSCHIEDENEN SOZIALEN SCHICHTEN ODER REGIONEN. NICHT ALLE MENSCHEN HABEN GLEICHERMAESSEN ZUGANG ZU MODERNER TECHNIK ODER EINER STABILEN INTERNETVERBINDUNG, WAS BILDUNGSUNGLEICHHEITEN VERSTAERKEN KANN. DIE MEDIZINISCHE TECHNOLOGIE HAT ENORME FORTSCHRITTE GEBRACHT. DIAGNOSTIK, BEHANDLUNGSMETHODEN UND MEDIKAMENTENENTWICKLUNG PROFITIEREN VON TECHNISCHEN INNOVATIONEN. TELEMEDIZIN ERMOEGLICHT ES, PATIENTEN AUCH IN ENTLEGENEN GEBIETEN MEDIZINISCH ZU BETREUEN. ZUGLEICH WIRFT DER EINSATZ VON TECHNOLOGIE ETHISCHE FRAGEN AUF, ETWA IM BEREICH DATENSCHUTZ ODER BEI DER ANWENDUNG VON KUENSTLICHER INTELLIGENZ IN DER MEDIZIN. DIE BALANCE ZWISCHEN FORTSCHRITT UND ETHISCHER VERANTWORTUNG IST HIER BESONDERS WICHTIG. TECHNOLOGIE KANN AUCH ZUR LOESUNG VON UMWELTPROBLEMEN BEITRAGEN. ERNEUERBARE ENERGIEN, INTELLIGENTE STROMNETZE UND UMWELTFREUNDLICHE PRODUKTIONSMETHODEN SIND BEISPIELE DAFUER, WIE TECHNISCHE INNOVATIONEN NACHHALTIGE ENTWICKLUNG FOERDERN KOENNEN. ABER DIE PRODUKTION UND ENTSORGUNG VON ELEKTRONIK VERURSACHT AUCH UMWELTBELASTUNGEN. ELEKTROSCHROTT, RESSOURCENVERBRAUCH UND ENERGIEBEDARF SIND HERAUSFORDERUNGEN, DIE MIT DER VERBREITUNG TECHNISCHER GERAETE EINHERGEHEN. TECHNOLOGIE PRAEGT UNSERE GESELLSCHAFT IN VIELERLEI HINSICHT UND BIETET ZAHLREICHE CHANCEN FUER FORTSCHRITT UND VERBESSERUNG DER LEBENSQUALITAET. GLEICHZEITIG BRINGT SIE NEUE HERAUSFORDERUNGEN UND RISIKEN MIT SICH, DIE VERANTWORTUNGSVOLL GEHANDHABT WERDEN MUESSEN. ES IST WICHTIG, DEN TECHNOLOGISCHEN WANDEL AKTIV ZU GESTALTEN, UM EINE NACHHALTIGE, INKLUSIVE UND HUMANE ZUKUNFT ZU ERMOEGLICHEN.'


if __name__ == '__main__':
    fill_vigenere_matrix()
    text = TEXT
    password = 'AAWCBYQ'
    encoded_text = encode_text_vigenere(text, password)

    flag = True
    while flag:
        for password_length in get_best_key_lengths(get_clear_text(encoded_text)):
            print(decode_text_vigenere(
                encoded_text,
                get_vigenere_password(get_clear_text(encoded_text), password_length)
            ))
            input()
