# Aufgabe 1: CAMSHIFT (Teil 2) (4 Punkte)

* (Fortsetzung der Aufgabe 2 des vorangeganenen Übungsblattes)
* implementiere die Berechnung des Fensterzentrums, -größe und Objektorientierung wie im Paper
* tracke das Auto vom ersten zum letzten Frame
## Abgabe 1.1
* letztes Einzelbild im Video plus Overlay des Suchfensters

# Aufgabe 2: Hu-Momente (6 Punkte)

* lies das paper: http://www.sci.utah.edu/~gerig/CS7960-S2010/handouts/Hu.pdf
* implementiere die sieben Momente von Hu
* nimm an, wir suchen ein Symbol ('needle.png') in einem Bild voller Symbole ('haystack.png')
* berechne die sieben Momente für das gesuchte Symbol
* suche die bounding boxes der Symbole im Haystack (wenn ihr mögt auch gerne über Drittsoftware)
* bestimme für jedes Symbol im Haystack die Ähnlichkeit (oder den Abstand) seiner sieben Momente zu denen des gesuchten Symbols
## Abgabe 2.1
* plotte das Symbol mit der höchsten Ähnlichkeit (dem geringsten Abstand)
