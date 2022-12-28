# influx-node-exporter

This is a set of handlers to export some data to an influxdb, with the purpose of monitoring them via grafana.

This is developped in python3.

### Installation

Installation is rather straight forward 
* install poetry
* poetry install
* fill in the example.env_file and save it as .env
* adapt config.yaml to your needs
* run the systemd service (see below if you intend to run the service as a user)


```
# must add passwordless access to smartctl if ran as user
username    ALL = (root) NOPASSWD: /usr/sbin/smartctl
```