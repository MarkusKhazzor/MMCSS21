Projektaufgabe im Kurs ‚Mathematische Methoden der Computer-Graphik‘ im SS2021 von Markus Kühner, Matrikelnummer: 2606211
"Simulation einer Achterbahn mittels Bezier-Interpolation und Visualisierung differentialgeometrischer Größen"

Abhängigkeiten um das Projekt ausführen zu können:

    Python 3.8 --> https://www.python.org/downloads/release/python-379/ --> einfachster weg zur globalen python installation
    über den "Windows x86-64 executable installer" wizard

    Verwendete Packages:
        - numpy 1.21.2
        - matplotlib 3.4.3

    IDE:
        PyCharm Community Edition 2021.2.1

Anleitung:

    Mit dem ausführen der MyMatLabCoaster.py wird das programm gestartet. Dabei ließt der TrackReader.py wie über der Funktion
    "extract_rollercoaster_pillar_points" im "TackReader.py" dokumentiert, die Trackdateien ein.
    Sodass ein Fenster erscheint, welches unten Links die Achterbahn aus den eingelesenen Punkten modelliert anzeigt.
    Darauf wird ein Punkt animiert, der in der aktuellen Curvature eingefärbt ist und das frenetische dreibein an dieser Position.
    Mit Linksklick kann in dem Diagramm rotiert werden und mit Rechtsklick + den Mauszeiger nach Oben oder Unten bewegen wird gezoomed.
    Die Obere Reihe an Diagrammen zeigt von Links betrachtet zuerst die erste Ableitung (speed), die zweite Ableitung (Acceleration) und die dritte Ableitung (jerk).
    Unter der dritten Ableitung wird ebenfall die Torsion und darunter die Curvature angezeigt.


    Known Issues:
        Auf manchen PCs braucht es die Zeile "npl.use('Qt5Agg')" in "MyMatLabCoaster.py" um das extra Fenster erstellen zu können.
        Bei sonstigen Problemen bitte melden!

