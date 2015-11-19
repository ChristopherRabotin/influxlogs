#!/usr/local/bin/python2.7
# encoding: utf-8
'''
influxlogs -- Write into InfluxDB some logs.

cmd is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2015 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import os
import sys

from influxdb.client import InfluxDBClient

from core import process_log
import settings


__all__ = []
__version__ = 0.1

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = 'E: %s' % msg
    def __unicode__(self):
        return self.msg

def main(argv=None):
    '''
    For a given log file, store data into InfluxDB based on the handlers defined in the settings.
    '''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_shortdesc = __import__('__main__').__doc__.split('\n')[1]
    program_license = '''{}

  Created by Christopher Rabotin.

  Licensed under BSD-3.

  Distributed on an 'AS IS' basis without warranties
  or conditions of any kind, either express or implied.

USAGE
'''.format(program_shortdesc)

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version', action='version', version='Version {}.'.format(__version__))
        parser.add_argument('logfile', help='path to log file')

        # Process arguments
        args = parser.parse_args()
        if args.logfile[-4:] != '.log':
            raise ValueError('Currently only supports uncompressed log files.')

        # Check the settings.
        if len(settings.HANDLERS) == 0:
            raise ValueError('No Handlers are defined in the settings.')

        try:
            idbc = InfluxDBClient(**settings.INFLUXDB)
        except TypeError as e:
            raise TypeError('Could not initialize InfluxDBClient: {}.'.format(repr(e)))

        routing = {}
        for hdlr in settings.HANDLERS:
            routing[hdlr.Meta.regexp] = hdlr
            hdlr.Meta.series._client = idbc
            hdlr.Meta.series._bulk_size = 10
            hdlr.Meta.series._autocommit = True

        for log_line in open(args.logfile).readlines():
            for regexp, hdlr in routing.items():
                process_log(log_line, regexp, hdlr)

        # Let's commit whichever is remaining.
        for hdlr in settings.HANDLERS:
            hdlr.Meta.series.commit(idbc)

        return 0
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        raise e
        indent = len(program_name) * ' '
        sys.stderr.write('{}: {}\n'.format(program_name, repr(e)))
        sys.stderr.write(indent + '  for help use --help\n')
        return 2

if __name__ == '__main__':
    sys.exit(main())
