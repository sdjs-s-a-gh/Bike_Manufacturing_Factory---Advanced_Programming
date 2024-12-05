from Production_Class import production


class InputBin:
    def __init__(self):
        self.__frames: int = 0
        self.__forks: int = 0

    def get_details(self) -> list:
        items = [self.__frames, self.__forks]
        return items

    def set_frames(self, frames: int) -> None:
        self.__frames = frames

    def set_forks(self, forks: int) -> None:
        self.__forks = forks


class OutputBin:
    def __init__(self, productions: production):
        self.__components = productions.get_components()    # the list of components
        self.__components_dict = {component: 0 for component in self.__components}   # dictionary comprehension where each component is a key

    def get_components_list(self) -> list:
        return self.__components

    def get_components_dict(self) -> dict:
        return self.__components_dict

    def increment_component_count(self, component) -> None:
        self.__components_dict[component] += 1

    # on production of a bike
    def decrement_component_count(self, components: list) -> None:
        for component in components:
            self.__components_dict[component] -= 1
