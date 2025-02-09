# GSR-Sensor-Datenaufzeichnung mit InfluxDB auf Grafana (Option Docker / Webdesk mit flusk)

Dieses Python-Projekt misst die Hautleitfähigkeit (GSR - Galvanic Skin Response) mit einem Grove GSR-Sensor und speichert die Daten in InfluxDB. Die Messungen können über ein einfaches CLI-Menü gestartet und verwaltet werden.Die Messdaten werden von influxDB an einen grafana web client übergeben und in Echtzeit dargestellt. 

---

## Funktionen
**Erfassung von GSR-Sensordaten** über einen Grove GSR-Sensor  
**Berechnung der Leitfähigkeit** (Mikrosiemens) aus den Rohwerten  
**Speicherung der Messwerte in einer InfluxDB-Datenbank**  
**CLI-Menü für die Steuerung** der Messung  
**Automatische Fehlerbehandlung** für Sensor-Fehlmessungen  

---

## Installation

### **Abhängigkeiten installieren**
```bash
pip install influxdb grovepi

git clone https://github.com/DexterInd/GrovePi
cd GrovePi/Software/Python
pip install .

InfluxDB installieren & starten

Falls du InfluxDB noch nicht installiert hast, folge diesen Schritten:
Für Debian/Ubuntu

sudo apt update
sudo apt install influxdb
sudo systemctl start influxdb
sudo systemctl enable influxdb

Für macOS (Homebrew)

brew install influxdb
brew services start influxdb

influx
> CREATE DATABASE gsr_data
> EXIT

Konfiguration

Falls dein InfluxDB-Server nicht auf localhost:8086 läuft, ändere die Werte in INFLUXDB_HOST und INFLUXDB_PORT:

INFLUXDB_HOST = "localhost"  # Ändere auf deine InfluxDB-Adresse
INFLUXDB_PORT = 8086         # Standard-Port von InfluxDB
INFLUXDB_DB = "gsr_data"

## Nutzung

Starte das Programm mit:

python gsr_sensor.py

CLI-Menü

Das Programm startet mit einem Hauptmenü, in dem du:
1. Eine neue Messung starten kannst
2. Das Programm beenden kannst

Beispiel-Eingabe:

EDA-Messung - Hauptmenü
1. Neue Messung starten
2. Programm beenden
Wählen Sie eine Option: 1
Geben Sie die Messdauer in Sekunden ein: 30

Das Programm beginnt, die Hautleitfähigkeit alle 1/16 Sekunden zu messen und in InfluxDB zu speichern.

Daten in InfluxDB anzeigen

Öffne die InfluxDB CLI:

%influx

Zeige die letzten Messwerte an:

USE gsr_data;
SELECT * FROM gsr_measurement ORDER BY time DESC LIMIT 10;









