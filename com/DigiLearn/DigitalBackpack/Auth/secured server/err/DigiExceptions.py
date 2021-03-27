class DigiError(Exception):
    pass


class TrashedFileError(DigiError):
    """
        attributes
        expression - input expression in which the error occurred
        message - explanation of the error
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

