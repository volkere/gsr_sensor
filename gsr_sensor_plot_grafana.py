# -*- coding: utf-8 -*-
from grovepi import *
import time
import math
from datetime import datetime
from influxdb import InfluxDBClient

# Konfiguration des GSR-Sensors
GSR_SENSOR = 0  # Analoger Port A0
TR = 16  # Abtastrate
DT = 64 / TR
NN = 1920  # Maximaler Puffer für Daten
R_S = 51000  # Bekannter Widerstand in Ohm (51 kOhm)
V_IN = 5.0  # Versorgungsspannung des Sensors

# InfluxDB-Konfiguration
INFLUXDB_HOST = "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_DB = "gsr_data"

# InfluxDB-Client erstellen
client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT, database=INFLUXDB_DB)

# Benutzerfunktionen
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

def measure_and_send_to_influx(duration):
    """Messung der GSR-Werte und Senden an InfluxDB."""
    start_time = time.time()
    print("Messung läuft... Drücken Sie Strg+C zum Abbrechen.")

    try:
        while (time.time() - start_time) < duration:
            value = read_gsr()
            if value:
                conductivity = calculate_conductivity(value)
                timestamp = datetime.utcnow().isoformat()

                # Datenpunkt für InfluxDB erstellen
                data_point = [{
                    "measurement": "gsr_measurement",
                    "tags": {
                        "sensor": "GSR",
			"location": "Volker's Lab"
                    },
                    "time": timestamp,
                    "fields": {
                        "conductivity": float(conductivity),
			"raw_value": value
                    }
                }]

                client.write_points(data_point)

                print("Zeit: {:.2f}, Leitfähigkeit: {:.2f} µS".format(time.time() - start_time, conductivity))

            time.sleep(1.0 / TR)  # Abtastrate beachten

    except KeyboardInterrupt:
        print("Messung abgebrochen.")
    finally:
        print("Messung abgeschlossen.")

# Hauptprogramm
if __name__ == "__main__":
    while True:
        print("\nEDA-Messung - Hauptmenü")
        print("1. Neue Messung starten")
        print("2. Programm beenden")
        choice = raw_input("Wählen Sie eine Option: ")

        if choice == "1":
            duration = int(raw_input("Geben Sie die Messdauer in Sekunden ein: "))
            measure_and_send_to_influx(duration)
        elif choice == "2":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")

