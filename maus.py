# -*- coding: utf-8 -*-
from grovepi import *
import time
import math
from datetime import datetime
import matplotlib
matplotlib.use("Agg")  # Verwende ein nicht-interaktives Backend
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Konfiguration des GSR-Sensors
GSR_SENSOR = 0  # Analoger Port A0
TR = 16  # Abtastrate
DT = 64 / TR
NN = 1920  # Maximaler Puffer für Daten
R_S = 51000  # Bekannter Widerstand in Ohm (51 kOhm)
V_IN = 5.0  # Versorgungsspannung des Sensors

# Globale Variablen
timestamps = []
conductivities = []
output_file = "maus.crv"
plot_file = "maus.png"

# Benutzerfunktionen
def show_menu():
    print("\nEDA-Messung - Hauptmenü")
    print("1. Neue Messung starten")
    print("2. Daten anzeigen")
    print("3. Daten speichern")
    print("4. Programm beenden")
    choice = raw_input("Wählen Sie eine Option: ")
    return int(choice)

def read_gsr():
    """Lese den GSR-Wert vom Sensor."""
    try:
        value = analogRead(GSR_SENSOR)
        return value
    except IOError:
        print("Fehler beim Lesen des GSR-Sensors.")
        return None

def calculate_conductivity(raw_value):
    """Berechne die Hautleitfähigkeit in Mikrosiemens."""
    if raw_value == 0:
        return 0  # Vermeide Division durch Null
    v_out = (raw_value / 1023.0) * V_IN
    if v_out > 0:
        r_h = R_S * ((V_IN / v_out) - 1)
        if r_h > 0:
            return (1 / r_h) * 1e6  # Umrechnung in Mikrosiemens
    return 0

def measure_gsr(duration):
    """Messung der GSR-Werte."""
    start_time = time.time()
    print("Messung läuft...")
    while (time.time() - start_time) < duration:
        value = read_gsr()
        if value:
            conductivity = calculate_conductivity(value)
            conductivities.append(conductivity)
            timestamps.append(time.time() - start_time)
        time.sleep(1.0 / TR)  # Abtastrate beachten
    print("Messung abgeschlossen.")

def save_data():
    """Speichern der Hautleitfähigkeitsdaten in eine Datei."""
    with open(output_file, "w") as f:
        f.write("Timestamp,Conductivity(µS)\n")
        for t, c in zip(timestamps, conductivities):
            f.write("{:.2f},{}\n".format(t, c))
    print("Daten wurden in '{}' gespeichert.".format(output_file))

    # Plotte die Daten und speichere den Plot
    save_plot()

def save_plot():
    """Erstelle und speichere einen Plot der Hautleitfähigkeitsdaten."""
    plt.figure(figsize=(10, 6))

    # Daten für glatte Kurven vorbereiten
    timestamps_smooth = np.linspace(min(timestamps), max(timestamps), 500)
    conductivities_interpolator = interp1d(timestamps, conductivities, kind="cubic")
    conductivities_smooth = conductivities_interpolator(timestamps_smooth)

    # Plot für die Hautleitfähigkeit
    plt.plot(timestamps_smooth, conductivities_smooth, label=u"Leitfähigkeit (µS)", color="green")
    plt.title(u"Hautleitfähigkeit")
    plt.xlabel(u"Zeit (s)")
    plt.ylabel(u"Leitfähigkeit (µS)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig(plot_file)
    print("Plot wurde in '{}' gespeichert.".format(plot_file))

def show_data():
    """Anzeige der erfassten Hautleitfähigkeitsdaten."""
    print("\nErfasste Daten:")
    for t, c in zip(timestamps, conductivities):
        print("Zeit: {:.2f} s, Leitfähigkeit: {:.2f} µS".format(t, c))

# Hauptprogramm
if __name__ == "__main__":
    while True:
        choice = show_menu()
        if choice == 1:
            duration = int(raw_input("Geben Sie die Messdauer in Sekunden ein: "))
            measure_gsr(duration)
        elif choice == 2:
            show_data()
        elif choice == 3:
            save_data()
        elif choice == 4:
            print("Programm beendet.")
            break
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")

