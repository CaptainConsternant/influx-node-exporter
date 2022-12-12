import socket

import yaml
from decouple import config
from influxdb import InfluxDBClient

from log import log


class Handler:
    def __init__(self, *args, **kwargs):
        self.config = yaml.safe_load(open("config.yaml"))[self.__class__.__name__]
        self.database_name = self.config["db_name"]
        self.host = socket.gethostname()

        self.client = InfluxDBClient(
            host=config("INFLUXDB_HOST", default="localhost"),
            port=config("INFLUXDB_PORT", default=8086),
            username=config("INFLUXDB_USERNAME", default="root"),
            password=config("INFLUXDB_PASSWORD", default="root"),
            ssl=config("INFLUXDB_SSL", default=False),
            verify_ssl=config("INFLUXDB_VERIFY_SSL", default=False),
        )
        self.client.create_database(self.database_name)
        self.client.switch_database(self.database_name)
        # TODO implement retention here
        # self.client.alter_retention_policy('autogen', self.database_name, duration=kwargs.get('duration','4w'))
        log.info(f"Successfully connected to {self.database_name}")

        self.data_buffer = []

    def collect(self):
        log.info("collect")
        """Main process to collect data"""
        raise NotImplementedError

    def write_buffer_to_db(self):
        """Write data points to influx"""
        for r in self.data_buffer:
            r["tags"]["host"] = self.host
        self.client.write_points(self.data_buffer)
        log.debug(f"saved {self.data_buffer}")
        self.data_buffer = []

    def run(self):
        """Runs main collect and write process. (Wrapper used for scheduling job purposes)
        This is launched by an APScheduler job, at an interval specified in config.yaml"""
        self.collect()
        self.write_buffer_to_db()

    def run_maintenance(self):
        """Some handlers require some regular maintenance, i.e. operations not destined to collect data,
        but rather to force update of said data (smart tests for instance).
        This is a way of managing them if not ran otherwise"""
        raise NotImplementedError
