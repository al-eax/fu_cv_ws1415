# Übung 5
## Aufgabe 1: Histogram of Oriented Gradients (10 Punkte)

* implementiere eine Funktion zur Extraktion eines Winkelhistogramms wie in der Vorlesung beschrieben (für Zellen der Größe 8 x 8 Pixel)
* benutze diese Funktion für die Extraktion des HOGs für die Organisationsebenen Blöcke und ROIs
* implementiere eine Funktion, die, gegeben ein Winkelhistogramm, die Hauptkantenrichtung in einem Block als weiße Linie auf schwarzem Hintergrund darstellt
* benutze diese Funktion, um das Eingabebild person.png als Mosaik aus diesen Hauptkantenrichtungskacheln darzustellen (Abgabe 1.1)
* implementiere die Suche nach Personen in beliebig großen Eingabebildern. Nimm dazu eine Suchfenstergröße von 144 x 384 Pixeln an. Suche in den Bildern people.png und people2.png nach Personen. Nutze für die Entscheidung, ob ein ROI eine Person enthält die Vorlage person.png. Stelle bei positivem Ergebnis das jeweilige ROI als Overlay auf dem Bild dar (Abgabe 1.2 und 1.3)
