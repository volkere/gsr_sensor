# -*- coding: utf-8 -*-
from grovepi import *
from datetime import datetime
import matplotlib
matplotlib.use("Agg")  # Verwende ein nicht-interaktives Backend
import matplotlib.pyplot as plt
import numpy as np  # Für polynomielle Anpassung
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
                print "[%s] WARNUNG: Sensor gibt konstante Werte zurück (65280)." % current_time
            else:
                print "[%s] GSR value: %d" % (current_time, value)

                # Speichere die Daten
                with open(output_file, "a") as file:
                    file.write("%s,%d\n" % (current_time, value))

                # Daten für den Plot hinzufügen
                timestamps.append(elapsed_time)
                values.append(value)

            # Reduziere die Wartezeit zwischen den Messungen
            time.sleep(0.1)

        except IOError:
            # Fehler bei der Kommunikation mit dem Sensor
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print "[%s] Fehler: Sensor konnte nicht gelesen werden." % current_time
except KeyboardInterrupt:
    # Beende das Programm und speichere den Plot
    print "\nMessung beendet. Daten gespeichert in", output_file

    # Erstelle den Plot
    plt.figure(figsize=(10, 6))

    # Zeichne die gemessenen Daten als Punkte
    plt.scatter(timestamps, values, label=u"GSR Werte", color="blue", alpha=0.7)

    # Berechne die Kleinste-Quadrate-Näherung (z. B. Polynom 2. Grades)
    if len(timestamps) > 1:
        coefficients = np.polyfit(timestamps, values, 2)  # Polynom 2. Grades
        poly_eq = np.poly1d(coefficients)
        regression_values = poly_eq(timestamps)

        # Zeichne die Kurve der Kleinste-Quadrate-Näherung
        plt.plot(timestamps, regression_values, label=u"Kleinste-Quadrate-Kurve", color="red", linewidth=2)

    # Beschrifte den Plot
    plt.title(u"GSR Sensor Data mit Kleinste-Quadrate-Näherung")
    plt.xlabel(u"Time (s)")
    plt.ylabel(u"GSR Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Speichere den Plot als PNG-Datei
    plt.savefig("gsr_plot_least_squares.png")
    print "Plot gespeichert als gsr_plot_least_squares.png"

