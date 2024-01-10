from ..exceptions import BaseServiceException

__all__ = (
    "IncorrectVariogramException",
    "IncorrectKrigingException",
    "KrigingNotCompletedException",
)


class IncorrectVariogramException(BaseServiceException):
    """
    Некорректная вариограмма
    """

    message = "Incorrect variogram"

    def __init__(self):
        super(self.__class__, self).__init__(self.message)


class IncorrectKrigingException(BaseServiceException):
    """
    Некорректная модель кригинга
    """

    message = "Incorrect kriging model"

    def __init__(self):
        super(self.__class__, self).__init__(self.message)


class KrigingNotCompletedException(BaseServiceException):
    """
    Процесс кригинга еще не завершен
    """

    message = "The kriging process has not been completed yet"

    def __init__(self):
        super(self.__class__, self).__init__(self.message)
