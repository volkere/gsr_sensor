# -*- coding: utf-8 -*-
from grovepi import *
from datetime import datetime
import matplotlib
matplotlib.use("Agg")  # Verwende ein nicht-interaktives Backend
import matplotlib.pyplot as plt
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

            # Kurze Pause, um Sensor nicht zu überlasten
            time.sleep(0.5)

        except IOError:
            # Fehler bei der Kommunikation mit dem Sensor
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print "[%s] Fehler: Sensor konnte nicht gelesen werden." % current_time
except KeyboardInterrupt:
    # Beende das Programm und speichere den Plot
    print "\nMessung beendet. Daten gespeichert in", output_file

    # Erstelle den Plot und speichere ihn
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, values, label="GSR Value", color="blue", linewidth=2)
    plt.title("GSR Sensor Data")
    plt.xlabel("Time (s)")
    plt.ylabel("GSR Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Speichere den Plot in eine PNG-Datei
    plt.savefig("gsr_plot_curve.png")
    print "Plot gespeichert als gsr_plot.png"

