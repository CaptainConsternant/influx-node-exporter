import yaml
from decouple import config
from influxdb import InfluxDBClient

from log import log


class Handler:
    def __init__(self, *args, **kwargs):
        self.config = yaml.safe_load(open("config.yaml"))[self.__class__.__name__]
        self.database_name = self.config["db_name"]

        # TODO implement >>> client = InfluxDBClient(host='mydomain.com', port=8086, username='myuser', password='mypass' ssl=True, verify_ssl=True)
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
        # self.client.alter_retention_policy('autogen', self.database_name, duration=kwargs.get('duration','4w'))
        log.info(f"Successfully connected to {self.database_name}")

        self.data_buffer = []

    def collect(self):
        raise NotImplementedError

    def write_buffer_to_db(self):
        self.client.write_points(self.data_buffer)
        self.data_buffer = []

    def run(self):
        self.collect()
        self.write_buffer_to_db()
