# ##
# InfluxLogs settings
# ##
from os import getenv

from heroku import HerokuRouter


# Handlers is a list of handlers. Make sure they are imported.
HANDLERS = [HerokuRouter]

# InfluxDB CONFIG
INFLUXDB = {'host': getenv('INFLUXDB_HOST'),
            'port': getenv('INFLUXDB_PORT'),
            'username': getenv('INFLUXDB_USER'),
            'password': getenv('INFLUXDB_PWD'),
            'database': getenv('INFLUXDB_DB')}
