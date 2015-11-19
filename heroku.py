from core import LogHandler
from influxdb.helper import SeriesHelper

class RouterSeries(SeriesHelper):
    class Meta:
        series_name = 'logs.heroku.{host}'
        fields = ['time', 'connect', 'service', 'bytes']
        tags = ['method', 'path', 'host', 'status']

class HerokuRouter(LogHandler):

    class Meta:
        regexp = r'heroku\[router\]:'
        series = RouterSeries

    @staticmethod
    def process(timestamp, log):
        data = {'time': timestamp}
        for section in log.split():
            try:
                param, value = section.split('=')
            except IndexError:
                print('WARNING: Do not know how to parse {}.'.format(section))
            else:
                if param in RouterSeries.Meta.fields + RouterSeries.Meta.tags:
                    data[param] = value.replace('"', '').replace('ms', '')

        RouterSeries(**data)
