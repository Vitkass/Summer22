from setuptools import setup, find_packages

setup(
    name='Robin.Files.FileCopy-Python',
    version='1.5.3',
    packages=find_packages(),
    package_data={
        '': ['*.robin-impinfo']
    },
    python_requires='~=3.8',
    install_requires=[
        'Robin.ActionSDK==1.5.9',
        'Robin.Type.FilePath==1.0.0',
        'Robin.Type.FolderPath==1.0.0',
    ],
    url='http://robingit.itbs.it.ru/actions/python-actions/files_actions',
    author='Dmitry Zimoglyadov',
    author_email='DZimoglyadov@rpa-robin.ru',
    description='Create a copy of a specified file'
)
