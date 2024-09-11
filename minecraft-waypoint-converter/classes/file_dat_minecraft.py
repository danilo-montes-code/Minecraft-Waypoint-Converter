"""file_dat_minecraft.py

Contains a class that handles Minecraft dat file IO.
"""

# python native
from typing import Any
import amulet_nbt
from amulet_nbt import NamedTag

# in project
from .file_extension import FileExtension
from .useful_methods import *


class MinecraftDatFile(FileExtension):
    """
    Class that handles txt file IO.

    Attributes
    ----------
    fn : str
        filename of the file
    
    Methods
    -------
    read():
        opens the file and returns its data
    write(data):
        writes data to file
    print():
        opens the file and prints the data
    """

    def __init__(self, fn: str) -> None:
        """
        Creates MinecraftDatFile instance.

        Attributes
        ----------
        fn : str
            filename of the desired file
        """

        super().__init__(fn = fn, extension_suffix = '.dat')


    def read(self) -> list[str] | None:
        """
        Opens dat file and returns its data.

        Returns
        -------
        list[str]
            the data contained in the file | 
            None is there was an error
        """

        data = None
        try:
            data = amulet_nbt.load(self.fn)

        except IOError as e:
            handle_error(e, 'MinecraftDatFile.open()',
                         'error opening file')

        except Exception as e:
            handle_error(e, 'MinecraftDatFile.open()', 
                         'erroneous error opening file')

        finally:
            return data
        

    def write(self, data: list[str]) -> bool:
        """
        Writes data to dat file. Overwrites all data held in file.

        Parameters
        ----------
        data : list[str]
            the data to write to the file

        Returns
        -------
        bool
            True,  if the data was written to the file |
            False, otherwise
        """

        saved = False
        try: 
            with open(self.fn, 'w') as f:
                f.writelines(line + '\n' for line in data)
                saved = True
        
        except Exception as e:
            handle_error(e, 'MinecraftDatFile.write()', 'error writing to file')

        finally:
            return saved
        
    
    def print(self) -> None:
        """
        Opens the dat file and prints the data.
        """
        
        data = self.read()
        print(data)