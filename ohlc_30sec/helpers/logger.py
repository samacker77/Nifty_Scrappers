import logging

def return_logger():
    '''
    Summary Line
    ------------
        Returns logger object

    :param:
        None
    :return:
        logger object
    '''
    logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s')
    logging.root.setLevel(logging.NOTSET)
    logger = logging.getLogger('nifty-ohlc')
    logger.setLevel(logging.INFO)
    return logger
