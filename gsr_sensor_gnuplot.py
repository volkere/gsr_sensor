# -*- coding: utf-8 -*-
from grovepi import *
from datetime import datetime
import gnuplotlib as gp  # Verwende Gnuplotlib für das Plotten
import numpy as np
import time

# Definiere den Port, an dem der GSR-Sensor angeschlossen ist
sensor_port = 0  # A0

# Initialisiere Listen für die Daten
timestamps = []
values = []

# Datei zum Speichern der Daten
output_file = "gsr_data.csv"

# Schreibe die Kopfzeile in die Datei
with open(output_file, "w") as file:
    file.write("Timestamp,GSR Value\n")

print "Starte den Test für den GSR-Sensor (Python 2)"
start_time = time.time()

try:
    while True:
        try:
            # Lese den analogen Wert vom GSR-Sensor
            value = analogRead(sensor_port)

            # Hol die aktuelle lokale Zeit
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            elapsed_time = time.time() - start_time  # Zeit seit Start in Sekunden

            # Prüfe auf typische Fehlerwerte
            if value == 65280:
                print "[{}] WARNUNG: Sensor gibt konstante Werte zurück (65280).".format(current_time)
            else:
                print "[{}] GSR value: {}".format(current_time, value)

                # Speichere die Daten
                with open(output_file, "a") as file:
                    file.write("{},{}\n".format(current_time, value))

                # Daten für den Plot hinzufügen
                timestamps.append(elapsed_time)
                values.append(value)

            # Reduziere die Wartezeit zwischen den Messungen
            time.sleep(0.01)

        except IOError:
            # Fehler bei der Kommunikation mit dem Sensor
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print "[{}] Fehler: Sensor konnte nicht gelesen werden.".format(current_time)
except KeyboardInterrupt:
    # Beende das Programm und speichere den Plot
    print "\nMessung beendet. Daten gespeichert in", output_file

    # Erstelle eine Kleinste-Quadrate-Näherung (z. B. Polynom 2. Grades)
    if len(timestamps) > 1:
        # Berechnung der Koeffizienten für ein Polynom 2. Grades
        coefficients = np.polyfit(timestamps, values, 2)
        poly_eq = np.poly1d(coefficients)
        regression_values = poly_eq(timestamps)

        # Zeichne die Punkte und die Kleinste-Quadrate-Kurve mit Gnuplotlib
        gp.plot(
            (timestamps, values, {"with": "points", "title": "GSR Werte", "pointtype": 7}),
            (timestamps, regression_values, {"with": "lines", "title": "Kleinste-Quadrate-Kurve", "linewidth": 2}),
            _set="title 'GSR Sensor Data mit Kleinste-Quadrate-Näherung'; xlabel 'Time (s)'; ylabel 'GSR Value'",
            terminal="png size 1024,768",
            output="gsr_plot_least_squares.png"
        )
        print "Plot gespeichert als gsr_plot_least_squares.png"

