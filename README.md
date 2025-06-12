
# 📘 Benutzerdokumentation: Vigenère-Entschlüssler

## Zweck der Software

Diese Anwendung entschlüsselt deutsche Texte, die mit der Vigenère-Verschlüsselung codiert wurden, **ohne das Passwort zu kennen**.

Sie liest den verschlüsselten Text aus einer Datei ein, ermittelt die Passwortlänge statistisch und nutzt die Buchstabenhäufigkeiten, um mögliche Klartexte zu erzeugen. Nach jedem Versuch werden die ersten 80 Zeichen des Ergebnisses angezeigt.

So ermöglicht das Programm die automatisierte Entschlüsselung von Vigenère-verschlüsselten Texten.

---

## Schnellstart

1. **Programm starten**  
   Führen Sie die Datei `main.py` aus. Dies kann z. B. über das Terminal erfolgen:

   ```bash
   python main.py
   ```

2. **Textdatei auswählen**  
   Es öffnet sich ein Dateidialog. Wählen Sie die verschlüsselte Textdatei im `.txt`-Format aus, die Sie entschlüsseln möchten.

3. **Entschlüsselung bewerten**  
   Das Programm schlägt automatisch mehrere mögliche Entschlüsselungen vor. Nach jeder Variante werden Sie gefragt:

   > _„Sieht dieser Text wie ein deutscher Klartext aus?“_

   Antworten Sie mit `j` für „ja“ oder `n` für „nein“.

4. **Ergebnis speichern**  
   Sobald ein sinnvoller Text erkannt wurde, werden Sie gebeten, eine Zieldatei für den entschlüsselten Text auszuwählen.

5. **Abschluss**  
   Das gefundene Passwort wird angezeigt und der entschlüsselte Text wird in der gewünschten Datei gespeichert.


---

## Eingabe & Ausgabe

| Typ     | Beschreibung                                               |
|----------|------------------------------------------------------------|
| **Eingabe** | Textdatei (.txt) mit Vigenère-verschlüsseltem Text         |
| **Ausgabe** | Textdatei (.txt) mit entschlüsseltem Inhalt (z. B. `entschluesselt.txt`) |

---

## Hinweise zur Software

- Das Programm berücksichtigt nur die Buchstaben A–Z (Groß- und Kleinbuchstaben). Alle anderen Zeichen, einschließlich Umlaute und Sonderzeichen, werden ignoriert bzw. übersprungen. Umlaute wie Ä, Ö, Ü sowie ß sollten vor der Verschlüsselung idealerweise in AE, OE, UE bzw. SS umgewandelt werden, damit sie richtig verarbeitet werden können.

- Für eine erfolgreiche Entschlüsselung ist die Passwortlänge entscheidend: Das Passwort muss mindestens 100-mal kürzer als der Text sein, also gilt `1 <= Passwortlänge <= Textlänge / 100`. Nur dann ist eine statistische Analyse der Buchstabenhäufigkeiten zuverlässig möglich. Wenn das Passwort fast so lang ist wie der Text, ist eine Entschlüsselung mit diesen Methoden praktisch nicht möglich, da keine ausreichenden Wiederholungen zur Analyse vorliegen.

---

# Methodendokumentation

Diese Software dient der Entschlüsselung von Texten, die mit dem **Vigenère-Verfahren** verschlüsselt wurden. Grundlage der Entschlüsselung ist die **statistische Analyse der Sprache**, insbesondere mit dem **Koinzidenzindex** und dem **Chi-Quadrat-Test**, um die wahrscheinlichste Passwortlänge und die dazugehörigen Buchstaben des Schlüssels zu bestimmen.

---

## 1. Vigenère-Verschlüsselung: Beispiel und Prinzip

Die Vigenère-Verschlüsselung ist ein **polyalphabetisches Substitutionsverfahren**, das ein Passwort verwendet, um jeden Buchstaben des Klartexts mit einer anderen Caesar-Verschiebung zu verändern.

### Beispiel

**Klartext**:  
```
DIESISTGEHEIM
```

**Passwort**:  
```
ABC
```

Zuerst wird das Passwort über den Text gelegt (zyklisch wiederholt):

```
D I E S I S T G E H E I M
A B C A B C A B C A B C A
```

Dann wird jeder Buchstabe des Klartexts durch den entsprechenden Buchstaben im Passwort verschlüsselt. Dabei entspricht:
- A = Verschiebung um 0
- B = Verschiebung um 1
- C = Verschiebung um 2

Beispiel für die Verschlüsselung:
- D + A = D
- I + B = J
- E + C = G
- ...

→ Ergebnis: `DJGSJU...`

---

## 2. Koinzidenzindex (KI)

Der **Koinzidenzindex** misst die Wahrscheinlichkeit, dass zwei zufällig gewählte Buchstaben im Text gleich sind.

### Allgemeine Formel

Für einen Text mit den Häufigkeiten $f_i$ jedes Buchstabens $i$ und Gesamtlänge $N$:

$$
KI = \frac{\sum_{i=1}^{26} f_i (f_i - 1)}{N (N - 1)}
$$

Typische Werte:
- **Deutsch**: ca. **0,078**
- **Zufälliger Text**: ca. **0,038**

### Vorgehen in der Software

Um die wahrscheinlichste Passwortlänge zu finden:

1. Iteration über alle Längen $L$ von $1$ bis $\text{Textlänge} / 100$
2. Für jede Länge:
   - Aufteilung des Textes in $L$ Spalten
   - Berechnung des KI jeder Spalte
   - Durchschnitt aller Spalten-KI-Werte
3. Berechnung der Differenz zum deutschen KI:

$$
\Delta(L) = |KI_{gemessen} - 0{,}078|
$$

4. Sortierung der Längen nach $\Delta(L)$ – je **kleiner**, desto **wahrscheinlicher** korrekt.

---

## 3. Chi-Quadrat-Test zur Caesar-Verschiebung

Jede der $L$ Spalten wird einzeln betrachtet und als Caesar-Verschlüsselung analysiert.

### Formel

$$
\chi^2 = \sum_{i=1}^{26} \frac{(O_i - E_i)^2}{E_i}
$$

- $O_i$: Beobachtete Häufigkeit des Buchstabens $i$
- $E_i$: Erwartete Häufigkeit in deutscher Sprache

Für jede Caesar-Verschiebung (0–25) wird $\chi^2$ berechnet. Die Verschiebung mit dem kleinsten $\chi^2$ wird gewählt.

### Visualisierung (Beispiel)

```
Verschiebung:    0   1   2   3   4   5
Chi²-Wert:      45  23  15   5  12  30

→ Minimum bei Verschiebung 3 ⇒ beste Übereinstimmung mit Deutsch
```

---

## Zusammenfassung der Verfahren

| Methode                  | Beschreibung                                                                 |
|--------------------------|-------------------------------------------------------------------------------|
| Vigenère-Verschlüsselung | Polyalphabetisches Verfahren mit periodischer Caesar-Verschlüsselung         |
| Koinzidenzindex (KI)     | Statistisches Maß zur Erkennung typischer Sprachmuster                       |
| Chi-Quadrat-Test         | Vergleich von Buchstabenverteilungen zur Caesar-Schlüsselbestimmung          |
| Durchschnitts-KI-Differenz | Grundlage zur Priorisierung der wahrscheinlichsten Passwortlängen             |
