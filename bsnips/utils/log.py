import logging
from logging import Formatter, Handler, Filter
from logging import StreamHandler
from logging.handlers import RotatingFileHandler


# Define some logging formats
main_formatter = Formatter('%(asctime)s - %(name)s - %(levelname)-8s - %(message)s')
simple_formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
verbose_formatter = Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(process)d - %(thread)d - %(message)s'
)


def config_handler(handler_class, level=logging.DEBUG, formatter=main_formatter, *args):
    handler = handler_class(*args)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def config_logger(name, level, handler=None, log_filter=None):
    l = logging.getLogger(name)
    l.setLevel(level)
    if handler is not None:
        if isinstance(handler, Handler):
            l.addHandler(handler)
        else:  # Enable adding more than one handler
            for h in handler:
                l.addHandler(h)
    if log_filter is not None:
        if isinstance(log_filter, Filter):
            l.addFilter(log_filter)
        else:  # Enable adding more than one filter
            for lf in log_filter:
                l.addFilter(lf)
    return l


def config_RFH(filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0):
    return config_handler(
        RotatingFileHandler, 0, main_formatter, filename, mode, maxBytes,
        backupCount, encoding, delay
    )


def setup_logging(level=10):
    """Setup a basic logging config, to stdout.
    :param level: the int value of the logging.X predefined variables,
        where X is one of:
            CRITICAL = 50
            ERROR = 40
            FATAL = 50
            WARN = 30
            INFO = 20
            DEBUG = 10
            NOTSET = 0
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    # Define some handlers
    rfh = config_handler(RotatingFileHandler, 0, main_formatter, 'rfh.log')
    rfh2 = config_RFH('rfh2.log', maxBytes=1024, backupCount=1)
    sh = config_handler(StreamHandler)
    log.addHandler(sh)
    log.addHandler(rfh)
    log.debug('debug message')
    log.info('info message')
    log.warn('warn message')
    log.error('error message')
    log.critical('critical message')

    log2 = config_logger('custom', 1, [rfh, sh, rfh2])
    log2.debug('debug message')
    log2.info('info message')
    log2.warn('warn message')
    log2.error('error message')
    log2.critical('critical message')
