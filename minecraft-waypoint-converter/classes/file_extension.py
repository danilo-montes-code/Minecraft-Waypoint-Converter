"""file_extension.py

Contains a class that handles file IO for a specific file format.
Class is written as an abstract class.
"""

# python native
import os
from abc import ABC, abstractmethod
from typing import Any


class FileExtension(ABC):
    """
    A class that handles file IO for a specific file format.
    
    Attributes
    ----------
    fn : str
        filename of the file
    extension_suffix : str
        the suffix of the file extension

    Methods
    -------
    open():
        opens the file and returns its data
    write(data):
        writes data to file
    """

    def __init__(self, fn : str, extension_suffix : str) -> None:
        """
        Creates FileExtension instance.

        Parameters
        ----------
        fn : str
            filename of the desired file
        extension_suffix : str
            the suffix of the file extension
        """
        
        self.fn = fn
        self.extension_suffix = extension_suffix
    
    
    
    @abstractmethod
    def read(self) -> Any:
        """
        Opens the file and returns the data held within.
        """
        pass

    
    @abstractmethod
    def write(self, data: Any) -> bool:
        """
        Writes to the file.
        """
        pass

    @abstractmethod
    def print(self) -> None:
        """
        Opens the file and prints the data held within.
        """
        pass


    def get_extension_suffix(self) -> str:
        return self.extension_suffix