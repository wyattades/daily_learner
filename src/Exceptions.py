
class ToSmallDataSetException(Exception):
    def __init__(self, message):
        super(ToSmallDataSetException, self).__init__(message)


class IncorrectPredictSizeException(Exception):
    def __init__(self, message):
        super(ToSmallDataSetException, self).__init__(message)