# generated by robin-py-toolset:
#   please avoid to edit this file
#   timestamp: 2022-01-31 18:42:09.088373

import pathlib
from typing import Any, Union

from EngineActionInterface.RobinExceptions import ActionException

# Import Robin Types:
from RobinFolderPath.RobinFolderPath import RobinFolderPath
from RobinFilePath.RobinFilePath import RobinFilePath


class RobinValidationErrorException(ActionException):
    """ Параметры не соотвествуют внутренним ограничениям алгоритма, например, выход за границы диапазона либо противоречивое сочетание параметров. Robin ID: Robin.Exception.ValidationError"""

    exception_id = 'Robin.Exception.ValidationError'
    message_text = 'Заданные значения параметров не позволяют выполнить действие'
    schema_version = '2.0.0'

    def __init__(self, 
            message: str = "", 
            *,
            parameter_name: str,
            **kwargs) -> None:
        
        assert isinstance(parameter_name, str), \
            f'Parameter parameter_name should be "str" but "{type(parameter_name)}" found'

        message = message or f"{self.__class__.message_text}: { parameter_name }"
        
        self.info = dict(
            parameter_name=parameter_name,
        )

        super().__init__(message, exception_id=self.__class__.exception_id, **kwargs)


class RobinDirectoryNotAvailableException(ActionException):
    """ Ошибка возникает, когда системе не удается получить доступ папке по указанному пути. Robin ID: Robin.Exception.DirectoryNotAvailable"""

    exception_id = 'Robin.Exception.DirectoryNotAvailable'
    message_text = 'Папка недоступна'
    schema_version = '2.0.0'

    def __init__(self, 
            message: str = "", 
            *,
            folder_path: str,
            **kwargs) -> None:
        
        assert isinstance(folder_path, str), \
            f'Parameter folder_path should be "str" but "{type(folder_path)}" found'

        message = message or f"{self.__class__.message_text}: { folder_path }"
        
        self.info = dict(
            folder_path=RobinFolderPath(valueOf_=folder_path),
        )

        super().__init__(message, exception_id=self.__class__.exception_id, **kwargs)


class RobinDirectoryNotFoundException(ActionException):
    """ Ошибка возникает, когда системе не удается найти папку в файловой системе по указанному пути. Robin ID: Robin.Exception.DirectoryNotFound"""

    exception_id = 'Robin.Exception.DirectoryNotFound'
    message_text = 'Папка не найдена'
    schema_version = '2.0.0'

    def __init__(self, 
            message: str = "", 
            *,
            folder_path: str,
            **kwargs) -> None:
        
        assert isinstance(folder_path, str), \
            f'Parameter folder_path should be "str" but "{type(folder_path)}" found'

        message = message or f"{self.__class__.message_text}: { folder_path }"
        
        self.info = dict(
            folder_path=RobinFolderPath(valueOf_=folder_path),
        )

        super().__init__(message, exception_id=self.__class__.exception_id, **kwargs)


class RobinFileNotFoundException(ActionException):
    """ Ошибка возникает, когда системе не удается найти файл в файловой системе по указанному пути. Robin ID: Robin.Exception.FileNotFound"""

    exception_id = 'Robin.Exception.FileNotFound'
    message_text = 'Файл не найден'
    schema_version = '2.0.0'

    def __init__(self, 
            message: str = "", 
            *,
            file_path: str,
            **kwargs) -> None:
        
        assert isinstance(file_path, str), \
            f'Parameter file_path should be "str" but "{type(file_path)}" found'

        message = message or f"{self.__class__.message_text}: { file_path }"
        
        self.info = dict(
            file_path=RobinFilePath(valueOf_=file_path),
        )

        super().__init__(message, exception_id=self.__class__.exception_id, **kwargs)


class RobinFileNotAvailableException(ActionException):
    """ Ошибка возникает, когда системе не удается получить доступ к файлу по указанному пути. Robin ID: Robin.Exception.FileNotAvailable"""

    exception_id = 'Robin.Exception.FileNotAvailable'
    message_text = 'Файл недоступен'
    schema_version = '2.0.0'

    def __init__(self, 
            message: str = "", 
            *,
            file_path: str,
            **kwargs) -> None:
        
        assert isinstance(file_path, str), \
            f'Parameter file_path should be "str" but "{type(file_path)}" found'

        message = message or f"{self.__class__.message_text}: { file_path }"
        
        self.info = dict(
            file_path=RobinFilePath(valueOf_=file_path),
        )

        super().__init__(message, exception_id=self.__class__.exception_id, **kwargs)

