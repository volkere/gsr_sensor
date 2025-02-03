# -*- coding: utf-8 -*-
from grovepi import *
from datetime import datetime

# Definiere den Port, an dem der GSR-Sensor angeschlossen ist
sensor_port = 0  # A0

print "Starte den Test für den GSR-Sensor (Python 2)"

while True:
    try:
        # Lese den analogen Wert vom GSR-Sensor
        value = analogRead(sensor_port)

        # Hol die aktuelle lokale Zeit
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Prüfe auf typische Fehlerwerte
        if value == 65280:
            print "[%s] WARNUNG: Sensor gibt konstante Werte zurück (65280)." % current_time
            print "Überprüfe die Verbindung und die GrovePi-Firmware."
        else:
            print "[%s] GSR value: %d" % (current_time, value)

    except IOError:
        # Fehler bei der Kommunikation mit dem Sensor
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print "[%s] Fehler: Sensor konnte nicht gelesen werden. Prüfe die Verbindung." % current_time

