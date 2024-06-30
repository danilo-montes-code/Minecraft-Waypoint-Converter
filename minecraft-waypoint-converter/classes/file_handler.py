"""file_handler.py

Contains class that handles a single file.
"""

# python native
import sys, os
from pathlib import Path
import ntpath
from typing import Any

# in project
from .file_extension import FileExtension
from .useful_methods import *


# constants
SCRIPT_ROOT = sys.path[0]


class FileHandler:
    """
    A class that handles a single file's input and output.

    Attributes
    ----------
    fn : str
        filename of the desired file
    extension : FileExtension
        handles file IO based on extension type
    
    Methods
    -------
    @staticmethod
    create_dir(path='data'):
        creates directory from the root directory at given path
    create_file():
        creates file at the location of the fn attribute
    file_exists():
        determines if file already exists
    is_empty():
        determines if file is empty
    read():
        opens file and returns its data
    write(data):
        writes to file
    print():
        opens file and prints its data
    """

    def __init__(self, 
                 extension : FileExtension, 
                 fn : str = None, 
                 dir : str = 'data',
                 full_path : str = None) -> None:
        """
        Creates FileHandler instance.

        Always provide `extension`.
        Either provide `fn` and optionally `dir`, or provide `full_path`.

        Parameters
        ----------
        extension : FileExtension
            handles file IO based on extension type
        fn : str, optional
            filename of the desired file, including extension
        dir : str, default='data'
            directory to put files in
        full_path : str, optional
            entire path of the file to handle, including extension
        """

        self.path = full_path or os.path.join(SCRIPT_ROOT, dir, fn)
        self.extention = extension(self.path)
        if not self.file_exists():
            if self.create_file():
                print_internal(f'{self.path} created successfully')
            else:
                print_internal(f'error creating file {self.path}')



    @classmethod
    def exact_path(cls,
                   full_path : str, 
                   extension : FileExtension):
        return cls(extension=extension, full_path=full_path)



    @staticmethod
    def create_dir(dir_path : str) -> bool: 
        """
        Create directory from the root of the script.

        Parameters
        ----------
        dir_path : str
            path of the directory to be created

        Returns
        -------
        bool
            True,  if directory was created successfully or if \
                   directory already exists |
            False, otherwise
        """

        created = False
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            created = True

        except FileExistsError:
            created = True

        except Exception as e:
            handle_error(e, 'FileHandler.create_dir()', 
                        'erroneous error creating data directory')

        finally:
            return created


    def create_file(self) -> bool:
        """
        Creates file at path specified in attribute.

        Returns
        -------
        bool
            True,  if file was created successfully |
            False, otherwise
        """

        file_created_successfully = False
        try:
            with open(self.path, 'a+'):
                file_created_successfully = True

        except FileNotFoundError as e:
            if not FileHandler.create_dir(os.path.dirname(self.path)):
                return False

            return self.create_file()

        except IOError as e:
            handle_error(e, 'FileHandler.create_file()', 
                         'error creating file')

        except Exception as e:
            handle_error(e, 'FileHandler.create_file()', 
                         'erroneous error creating file')

        return file_created_successfully
        

    def file_exists(self) -> bool:
        """
        Determines if file exists.

        Returns
        -------
        bool
            True,  if file exists |
            False, otherwise
        """

        return os.path.isfile(self.path)
    

    def is_empty(self) -> bool:
        """
        Determins if file is empty.

        Returns
        -------
        bool
            True,  if file is empty |
            False, otherwise
        """

        return os.stat(self.path).st_size == 0
    

    def read(self) -> Any | None:
        """
        Opens file and returns its data.

        Returns
        -------
        Any
            the data held in the file | 
            None, if file is empty
        """

        return self.extention.read() if not self.is_empty() else None
    

    def write(self, data: Any) -> bool:
        """
        Writes data to file.

        Parameters
        ----------
        data : Any
            data to write to the file
        
        Returns
        -------
        bool
            True,  if the data was written to the file successfully |
            False, otherwise
        """

        return self.extention.write(data)
    
    
    def print(self) -> None:
        self.extention.print()