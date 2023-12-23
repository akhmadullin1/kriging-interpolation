__all__ = (
    "BaseServiceException",
    "ItemNotFoundException",
)


class BaseServiceException(Exception):
    """
    Базовый класс исключения сервиса
    """


class ItemNotFoundException(BaseServiceException):
    """
    Не найден объект
    """

    message = "The object was not found"

    def __init__(self):
        super(self.__class__, self).__init__(self.message)
