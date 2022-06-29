import shutil
import os

from ActionSDK import BaseRobinAction
from ActionSDK.Utils import check_parameters

from RobinFilePath.RobinFilePath import RobinFilePath
from RobinFolderPath.RobinFolderPath import RobinFolderPath

from FileCopy.common.exceptions import \
    RobinFileNotAvailableException, \
    ActionException

from FileCopy.common.mixins import InOutMixin

from FileCopy.common.validators import FileValidator, DirectoryValidator

from typing import Any, Optional, Mapping


class FileCopy(BaseRobinAction, InOutMixin):

    # "Протокол" действия, свойство класса
    Parameters = dict(
        filePath=(True, RobinFilePath),
        targetPath=(True, RobinFolderPath),
        newFileName=(False, str),
        overwrite=(False, bool))

    Defaults = dict(
        newFileName='',
        overwrite=False,
    )
    Results = dict(
        # result=RobinFilePath
    )

    @check_parameters(**Parameters)
    def run_action(self) -> None:
        # Именованные аттрибуты, скалярные типы Python:
        params = self.get_params()        
        # Вызов ядра действия:
        self.file_copy(**params)

    def file_copy(self, *,
            filePath: str, 
            targetPath: str, 
            newFileName: str, 
            overwrite: bool) -> str:

        # #####################################################################
        # Валидация входных данных и подстановка значений по умолчанию
        # #####################################################################

        FileValidator.validate_file_path(filePath, parameter_name='filePath')

        if not newFileName:
            newFileName = os.path.basename(filePath)

        FileValidator.validate_file_path(newFileName, parameter_name='newFileName')

        if targetPath.endswith(os.path.sep):
            targetPath = targetPath[:-1]

        DirectoryValidator.validate_directory_path(targetPath, parameter_name='targetPath')

        new_file_path = os.path.join(targetPath, newFileName)

        # #####################################################################
        # Валидация ресурсов (существование, доступ)
        # #####################################################################

        FileValidator.validate_file_resource_r(filePath)

        DirectoryValidator.validate_directory_resource_w(targetPath)

        if not overwrite and os.path.exists(new_file_path):
            raise RobinFileNotAvailableException(
                f'Файл с именем "{new_file_path}" уже существует', 
                file_path=new_file_path)
        
        # #####################################################################
        # Выполнение операции
        # #####################################################################
        try:
            shutil.copy2(filePath, new_file_path)
        except Exception as ex:
            raise ActionException( 
                message=f'Невозможно выполнить операцию: {str(ex)}')

        return str(new_file_path)

