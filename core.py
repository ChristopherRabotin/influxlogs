"""
Meta class LogHandler for defining a log handler.
"""
import re


def process_log(log_line, regexp, hdlr):
    """
    Processes a given line from a log file for a given regular expression and handler.
    """
    try:
        first_match = re.findall(regexp, log_line)[0]
    except IndexError:
        pass
    else:
        timestamp = log_line.split(' ')[0]
        hdlr.process(timestamp, log_line[log_line.index(first_match) + len(first_match):].strip())


class LogHandler(object):
    """
    Subclassing this helper eases writing logs to InfluxDB.
    """

    __initialized__ = False
    def __new__(cls):
        """
        Initializes class attributes for subsequent constructor calls.
        """
        if not cls.__initialized__:
            cls.__initialized__ = True
            try:
                _meta = getattr(cls, 'Meta')
            except AttributeError:
                raise AttributeError(
                    'Missing Meta class in {}.'.format(
                        cls.__name__))

            try:
                cls._processor = getattr(cls, 'process')
            except AttributeError:
                raise AttributeError(
                    'Missing process function in {}.'.format(
                        cls.__name__))

            for attr in ['series', 'match']:
                try:
                    setattr(cls, '_' + attr, getattr(_meta, attr))
                except AttributeError:
                    raise AttributeError(
                        'Missing {} in {} Meta class.'.format(
                            attr,
                            cls.__name__))

        return super(LogHandler, cls).__new__(cls)
