from abc import ABC, abstractmethod

class GameObject(ABC):
    def __init__(self):
        self.is_alive = True

    @abstractmethod
    def draw(self):
        pass
