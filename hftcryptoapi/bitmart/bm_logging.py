class pyBitMartLog:
    logger_level = 'test'

    """:return true or false"""
    @staticmethod
    def is_debug():
        return pyBitMartLog.logger_level == 'debug'

    """
        :param
            logger_level: 'debug', 'info'
    """
    @staticmethod
    def set_logger_level(logger_level: str):
        pyBitMartLog.logger_level = logger_level


def log(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if pyBitMartLog.is_debug():
            print('response')
            print('\tbody:{}'.format(result[0]))
            print('\tlimit:{}'.format(result[1]))
        return result
    return wrapper