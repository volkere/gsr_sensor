
---

### `Dockerfile` für Sensor-Logger (`gsr_sensor.py`)**
```dockerfile
# Basis-Image mit Python
FROM python:3.9

WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code kopieren
COPY gsr_sensor.py .
COPY config.py .

# Start-Skript
CMD ["python", "gsr_sensor.py"]

