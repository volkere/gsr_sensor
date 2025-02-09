from flask import Flask, render_template
from influxdb import InfluxDBClient

app = Flask(__name__)

INFLUXDB_HOST = "influxdb"
INFLUXDB_PORT = 8086
INFLUXDB_DB = "gsr_data"

client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT, database=INFLUXDB_DB)

@app.route('/')
def index():
    query = "SELECT * FROM gsr_measurement ORDER BY time DESC LIMIT 10"
    result = client.query(query)
    data = list(result.get_points())

    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
