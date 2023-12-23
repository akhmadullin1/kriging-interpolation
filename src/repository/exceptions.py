__all__ = (
    "BaseRepoException",
    "ItemNotFoundInRepoException",
)


class BaseRepoException(Exception):
    """
    Базовый класс исключения репозитория
    """


class ItemNotFoundInRepoException(BaseRepoException):
    """
    Не найден объект в БД
    """

    message = "The object was not found in the database"

    def __init__(self):
        super(self.__class__, self).__init__(self.message)
