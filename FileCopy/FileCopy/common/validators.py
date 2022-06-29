# Желательно придерживаться единой реализации данного модуля 
# для всех действий файловой системы

import os

from pathlib import Path

from typing import Union

import platform

import string

import sys

import re

from .exceptions import \
    RobinFileNotFoundException, \
    RobinFileNotAvailableException, \
    RobinDirectoryNotFoundException, \
    RobinDirectoryNotAvailableException, \
    RobinValidationErrorException


StrPath = Union[Path, str]

OS_NAME = platform.system().lower()

INVALID_CHARS = '*?"<>|\t\n\r\x0b\x0c' + ''.join(chr(c) for c in range(128) if chr(c) not in string.printable)

INVALID_CHARS_PATTERN = f"[{re.escape(INVALID_CHARS):s}]"

INVALID_PATH_CHARS = re.compile(INVALID_CHARS_PATTERN, re.UNICODE)

class Validator:
    OS_NAME = platform.system().lower()

    @classmethod
    def is_windows(cls) -> bool:
        return cls.OS_NAME == 'windows'

    @classmethod
    def is_linux(cls) -> bool:
        return cls.OS_NAME == 'linux'

    @classmethod
    def validate_path_len(cls, p: StrPath) -> bool:
        if cls.is_windows:
            # Actually 260 up to Windows 10, 
            # the value 247 copied from .NET implementation for actions
            return len(str(p)) <= 247
        if cls.is_linux:
            return len(str(p)) <= 4096

    @classmethod
    def validate_filename_len(cls, p: StrPath) -> bool:
        if cls.is_windows:
            # Actually limitation exists for entire path
            return len(str(p)) <= 247
        if cls.is_linux:
            return len(str(p)) <= 255
    
    @classmethod
    def validate_path_chars(cls, p: StrPath) -> bool:
        # Включена по аналогии с .NET, 
        # делает отбраковку символов которые в принципе недопустимы в пути,
        # не учитывает особенности ОС,
        # встроенные функции .NET также не гарантируют 
        # окончательную проверку валидности символов
        stringified_name = str(p).replace('\\', '/')
        return not INVALID_PATH_CHARS.findall(stringified_name)

    @classmethod
    def check_read_access(cls, p: StrPath) -> bool:
        return os.access(str(p), os.R_OK)


    @classmethod
    def check_write_access(cls, p: StrPath) -> bool:
        return os.access(str(p), os.W_OK)

    @classmethod
    def check_exec_access(cls, p: StrPath) -> bool:
        return os.access(str(p), os.X_OK)

    @classmethod
    def check_file_locked(cls, p: StrPath) -> bool:
        # See also idea from: https://blogs.blumetech.com/blumetechs-tech-blog/2011/05/python-file-locking-in-windows.html
        file_path = str(p)
        if not (os.path.exists(file_path)):
            return False
        try:
            with open(file_path, 'r'):
                pass
        except IOError:
            return True
        return False
 

class DirectoryValidator(Validator):

    @classmethod
    def validate_directory_path(cls, p: StrPath, *, parameter_name: str) -> None:
        """Проверка валидности имени ресурса без проверки существования
        Raises: 
            RobinValidationErrorException
        """
        folder_path = str(p)

        if not cls.validate_path_len(folder_path):
            msg = f'Превышено ограничение на длину имени пути "{folder_path}"'
            raise RobinValidationErrorException(msg, parameter_name=parameter_name)
        
        # check valid symbols
        if not cls.validate_path_chars(p):
            msg = f'Недопустимые символы в имени пути "{folder_path}"'
            raise RobinValidationErrorException(msg, parameter_name=parameter_name)
        
    @classmethod
    def validate_directory_resource(cls, p: StrPath, *, check_write: bool=False, check_read: bool=False) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к директории
        Raises: 
            RobinDirectoryNotFoundException
            RobinDirectoryNotAvailableException
        """
        folder_path = str(p)

        if not os.path.exists(folder_path):
            msg = f'Директория "{folder_path}" не найдена'
            raise RobinDirectoryNotFoundException(msg, folder_path=folder_path)

        if not os.path.isdir(folder_path):
            msg = f'Ресурс "{folder_path}" не является директорией'
            raise RobinDirectoryNotFoundException(msg, folder_path=folder_path)
        
        if check_read and not cls.check_read_access(folder_path):
            msg = f'Ошибка доступа к "{folder_path}" для чтения'
            raise RobinDirectoryNotAvailableException(msg, folder_path=folder_path)

        if check_write and not cls.check_write_access(folder_path):
            msg = f'Ошибка доступа к "{folder_path}" для записи'
            raise RobinDirectoryNotAvailableException(msg, folder_path=folder_path)


    @classmethod
    def validate_directory_resource_r(cls, p: StrPath) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к директории (чтение)
        Raises: 
            RobinDirectoryNotFoundException
            RobinDirectoryNotAvailableException
        """
        cls.validate_directory_resource(p, check_read=True, check_write=False)

    @classmethod
    def validate_directory_resource_w(cls, p: StrPath) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к директории (запись)
        Raises: 
            RobinDirectoryNotFoundException
            RobinDirectoryNotAvailableException
        """
        cls.validate_directory_resource(p, check_read=False, check_write=True)

    @classmethod
    def validate_directory_resource_rw(cls, p: StrPath) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к директории (чтение/запись)
        Raises: 
            RobinDirectoryNotFoundException
            RobinDirectoryNotAvailableException
        """
        cls.validate_directory_resource(p, check_read=True, check_write=True)


class FileValidator(Validator):

    @classmethod
    def validate_file_path(cls, p: StrPath, *, parameter_name: str) -> None:
        """Проверка валидности имени ресурса без проверки существования
        Raises:
            RobinValidationErrorException
        """
        file_path = str(p)

        if not cls.validate_path_len(file_path):
            msg = f'Превышено ограничение на длину имени "{file_path}"'
            raise RobinValidationErrorException(msg, parameter_name=parameter_name)
        
        # check valid symbols
        if not cls.validate_path_chars(p):
            msg = f'Недопустимые символы в имени пути'
            raise RobinValidationErrorException(msg, parameter_name=parameter_name)

    @classmethod
    def validate_file_resource(cls, p: StrPath, *, check_write: bool=False, check_read: bool=False) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к файлу
        Raises:
            RobinFileNotFoundException
            RobinFileNotAvailableException
        """
        file_path = str(p)

        if not os.path.exists(file_path):
            msg = f'Файл "{file_path}" не найден'
            raise RobinFileNotFoundException(msg, file_path=file_path)

        if not os.path.isfile(file_path):
            # Python не имеет корректного аналога для кейса "не файл" - IsADirectory не всегда точно отражает суть
            msg = f'Ресурс "{file_path}" не является файлом'
            raise RobinFileNotFoundException(msg, file_path=file_path)
        
        if check_read and not cls.check_read_access(file_path):
            msg = f'Ошибка доступа к "{file_path}" для чтения'
            raise RobinFileNotAvailableException(msg, file_path=file_path)

        if check_write and not cls.check_write_access(file_path):
            msg = f'Ошибка доступа к "{file_path}" для записи'
            raise RobinFileNotAvailableException(msg, file_path=file_path)

    @classmethod
    def validate_file_resource_r(cls, p: StrPath) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к файлу (чтение)
        Raises:
            RobinFileNotFoundException
            RobinFileNotAvailableException
        """
        cls.validate_file_resource(p, check_read=True, check_write=False)

    @classmethod
    def validate_file_resource_w(cls, p: StrPath) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к файлу (запись)
        Raises:
            RobinFileNotFoundException
            RobinFileNotAvailableException
        """
        cls.validate_file_resource(p, check_read=False, check_write=True)

    @classmethod
    def validate_file_resource_rw(cls, p: StrPath) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к файлу (чтение/запись)
        Raises:
            RobinFileNotFoundException
            RobinFileNotAvailableException
        """
        cls.validate_file_resource(p, check_read=True, check_write=True)


class DirectoryTreeValidator(DirectoryValidator, FileValidator):

    @classmethod
    def validate_directory_resource(cls, p: StrPath, *, check_write: bool=False, check_read: bool=False) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к директории и вложенным файлам
        Raises: 
            RobinFileNotAvailableException
            RobinDirectoryNotFoundException
            RobinDirectoryNotAvailableException
        """
        folder_path = str(p)

        super().validate_directory_resource(p, check_read=check_read, check_write=check_write)

        for root, _, files in os.walk(folder_path, topdown=False):
            for name in files:
                fpath = os.path.join(root, name)

                if check_write and not cls.check_write_access(fpath):
                    msg = f'Недостаточно прав для записи "{fpath}"'
                    raise RobinFileNotAvailableException(msg, file_path=fpath)

                if check_read and not cls.check_read_access(fpath):
                    msg = f'Недостаточно прав для чтения "{fpath}"'
                    raise RobinFileNotAvailableException(msg, file_path=fpath)

                # Важно: проверка блокировки должна проводиться после проверки доступа
                if cls.check_file_locked(fpath):
                    msg = 'Невозможно совершить операцию,' + \
                            f' файл используется другим процессом: "{fpath}"'
                    raise RobinFileNotAvailableException(msg, file_path=fpath)
