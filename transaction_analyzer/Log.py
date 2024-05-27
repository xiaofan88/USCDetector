import logging

class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level='info',fmt='%(message)s'):


        self.logger = logging.getLogger(filename)

        self.logger.setLevel(self.level_relations.get(level))

        # th = logging.FileHandler(filename=filename, backupCount=backCount, encoding='utf-8')
        formatter = logging.Formatter(fmt)
        th = logging.FileHandler(filename=filename, encoding='utf-8')
        th.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(th)