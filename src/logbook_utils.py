import os

from logbook.more import ColorizingStreamHandlerMixin
from logbook import StreamHandler
from logbook.base import INFO, ERROR, NOTICE


class ColoredStreamHandler(ColorizingStreamHandlerMixin, StreamHandler):
    def should_colorize(self, record):
        if os.name == 'nt':
            try:
                import colorama
            except ImportError:
                return False
        return True

    def get_color(self, record):
        """Returns the color for this record."""
        if record.level >= ERROR:
            return 'red'
        elif record.level >= NOTICE:
            return 'yellow'
        elif record.level >= INFO:
            return ''
        return 'lightgray'
