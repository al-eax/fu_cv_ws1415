# Aufgabe 1: Scale Space (4 Punkte)

*    Lies das Paper von David Lowe (2004)
*    Implementiere den Scale Space und die Berechnung der DoG-Pyramide (benutze die Standardparameter, wie im Paper)
*    Stelle die unterste und oberste DoG-Schicht für das Eingabebild Lenna.png dar (Abgabe 1.1)

# Aufgabe 2: Keypoint-Detektion und Aussieben (4 Punkte)

*    Implementiere die Kandidatensuche
*    Implementiere die Aussortierung von Keypoints mit schwachem Kontrast und geringer Krümmung (die genaue Lokalisierung sparen wir uns hier)
*    Plotte die übrigen Keypoints auf dem Eingabebild als Kreise, deren Radii proportional zum scale sind (Abgabe 2.1)

# Aufgabe 3: Keypoint-Orientierung (4 Punkte)

*    Implementiere die Bestimmung der Keypoint-Orientierung (ohne Parabelfit)
*    Plotte die Keypoints aus 2. auf dem Eingabebild als Kreise, deren Radii proportional zum scale sind und zusätzlich einen Pfeil besitzen, der die Richtung des Keypoints widerspiegelt. (Abgabe 3.1)

# Aufgabe 4: Keypoint-Matching (4 Punkte)

*    Implementiere eine Funktion, die, gegeben zwei Keypoint-Mengen, korrespondierende Keypoints identifiziert.
*    Implementiere eine Funktion, die diese Korrespondenzen bildlich darstellt (z.B. als Linien, die die Keypoints in den beiden Bildern verbinden)
*    In den Dateien locs_X.csv und desc_X.csv sind Keypoints und Deskriptoren für die Bilder Lenna.png und Lenna_transformed.png gegeben. Stelle die Korrespondenzen grafisch dar. (Abgabe 4.1)
