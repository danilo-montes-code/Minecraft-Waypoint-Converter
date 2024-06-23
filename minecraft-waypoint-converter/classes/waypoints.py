from abc import ABC, abstractmethod

class Waypoints(ABC):

    def __init__(self) -> None:
        return


    @abstractmethod
    def get_worlds(self) -> list[str]:
        pass

    @abstractmethod
    def get_world_waypoints(self, 
                            world_name : str) -> list[str]:
        pass

    @abstractmethod
    def add_world_waypoints(self, 
                            world_name : str,
                            waypoints : list[str]) -> bool:
        pass

    @abstractmethod
    def world_in_list(self, world_name : str) -> bool:
        pass

    @abstractmethod
    def get_specific_world_name(self, search_name : str) -> list[str]:
        pass

    @abstractmethod
    def get_matching_servers(self, search_name : str) -> list[str]:
        pass

    @abstractmethod
    def choose_server(server_paths : list[str]) -> str:
        pass