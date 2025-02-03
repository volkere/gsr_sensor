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
smoothed_values = []  # Liste für geglättete Werte
conductivity_values = []  # Liste für Leitfähigkeitswerte
window_size = 5  # Fenstergröße für gleitendes Mittel

# Konstante für den bekannten Widerstand (in Ohm)
R_s = 51000  # 51 kΩ
V_in = 5.0  # Versorgungsspannung des Sensors (z. B. 5 V)

# Datei zum Speichern der Daten
output_file = "gsr_data.csv"

# Matplotlib für den Plot vorbereiten
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

# Plot für GSR Value
line1, = ax1.plot([], [], color='blue', label=u"GSR Value")
ax1.set_title(u"GSR Value Data")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel(u"GSR Value")
ax1.legend()
ax1.grid(True, which='both', linestyle='--', linewidth=0.5)
ax1.minorticks_on()

# Plot für Conductivity
line2, = ax2.plot([], [], color='green', label=u"GSR Conductivity (µS)")
ax2.set_title(u"GSR Conductivity Data")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel(u"Conductivity (µS)")
ax2.legend()
ax2.grid(True, which='both', linestyle='--', linewidth=0.5)
ax2.minorticks_on()

# Schreibe die Kopfzeile in die Datei
with open(output_file, "w") as file:
    file.write("Timestamp,GSR Value,Smoothed Value,Conductivity (µS)\n")

print "Starte den Test für den GSR-Sensor (Python 2)"
start_time = time.time()

while True:
    try:
        # Lese den analogen Wert vom GSR-Sensor
        raw_value = analogRead(sensor_port)

        # Berechne die Ausgangsspannung
        V_out = (raw_value / 1023.0) * V_in

        # Berechne den Hautwiderstand R_h
        if V_out > 0:  # Vermeide Division durch Null
            R_h = R_s * ((V_in / V_out) - 1)
        else:
            R_h = float('inf')  # Unendlich hoher Widerstand, falls keine Spannung

        # Berechne die Leitfähigkeit in Mikrosiemens
        if R_h > 0:
            conductivity = (1 / R_h) * 1e6  # Umrechnung in Mikrosiemens
        else:
            conductivity = 0.0

        # Hol die aktuelle lokale Zeit
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elapsed_time = time.time() - start_time  # Zeit seit Start in Sekunden

        # Prüfe auf typische Fehlerwerte
        if raw_value == 65280:
            print "[%s] WARNUNG: Sensor gibt konstante Werte zurück (65280)." % current_time
        else:
            print u"[%s] GSR value: %d, Conductivity: %.2f µS" % (current_time, raw_value, conductivity)

            # Speichere die Daten
            with open(output_file, "a") as file:
                file.write("%s,%d" % (current_time, raw_value))

            # Daten für den Plot hinzufügen
            timestamps.append(elapsed_time)
            values.append(raw_value)
            conductivity_values.append(conductivity)

            # Berechne gleitendes Mittel
            if len(values) >= window_size:
                smoothed_value = sum(values[-window_size:]) / window_size
                smoothed_values.append(smoothed_value)
                with open(output_file, "a") as file:
                    file.write(",%.2f,%.2f\n" % (smoothed_value, conductivity))
            else:
                smoothed_values.append(raw_value)  # Falls nicht genügend Werte vorliegen
                with open(output_file, "a") as file:
                    file.write(",%.2f,%.2f\n" % (raw_value, conductivity))

    except IOError:
        # Fehler bei der Kommunikation mit dem Sensor
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print "[%s] Fehler: Sensor konnte nicht gelesen werden." % current_time
    except KeyboardInterrupt:
        # Beende das Programm und speichere den Plot
        print "\nMessung beendet. Daten gespeichert in", output_file

        # Aktualisiere die Plots und speichere sie als PNG-Datei
        line1.set_xdata(timestamps)
        line1.set_ydata(values)
        ax1.relim()
        ax1.autoscale_view()

        line2.set_xdata(timestamps)
        line2.set_ydata(conductivity_values)
        ax2.relim()
        ax2.autoscale_view()

        # Zeichne den Plot und speichere ihn
        fig.canvas.draw()
        plt.tight_layout()
        plt.savefig("gsr_plot.png")  # Speichere den Plot als PNG-Datei
        print "Plot gespeichert als gsr_plot.png"
        break

