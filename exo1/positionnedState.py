from abc import ABC, abstractmethod
class PositionnedState(ABC):
    def __init__(self, positionnedState):
        self.positionnedState = positionnedState

    def on_enter(self, from_state: "PositionnedState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "PositionnedState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    # MOUVEMENT 1|0
    @abstractmethod
    def topLeft(self):
        pass

    @abstractmethod
    def topRight(self):
        pass

    @abstractmethod
    def bottomLeft(self):
        pass

    @abstractmethod
    def bottomRight(self):
        pass
    
     # utilitaire
    def _transition(self, new_state_cls: type["PositionnedState"], ):
        self.positionnedState.set_positionned_state(new_state_cls)


class TopLeft(PositionnedState):
    @property
    def name(self) -> str:
        return "TopLeft"
        
    def topLeft(self):
        print("le joueur est déjà en TopLeft")

    def topRight(self):
        self._transition(TopRight)

    def bottomLeft(self):
        self._transition(BottomLeft)

    def bottomRight(self):
        print("on ne peut pas aller en BottomRight depuis TopLeft")

class TopRight(PositionnedState):
    @property
    def name(self) -> str:
        return "TopRight"
        
    def topLeft(self):
        self._transition(TopLeft)

    def topRight(self):
        print("le joueur est déjà en TopRight")

    def bottomLeft(self):
        print("on ne peut pas aller en BottomLeft depuis TopRight")

    def bottomRight(self):
        self._transition(BottomRight)

class BottomLeft(PositionnedState):
    @property
    def name(self) -> str:
        return "BottomLeft"
        
    def topLeft(self):
        self._transition(TopLeft)

    def topRight(self):
        print("on ne peut pas aller en TopRight depuis BottomLeft")

    def bottomLeft(self):
        print("le joueur est déjà en BottomLeft")

    def bottomRight(self):
        self._transition(BottomRight)

class BottomRight(PositionnedState):
    @property
    def name(self) -> str:
        return "BottomRight"
        
    def topLeft(self):
        print("on ne peut pas aller en TopLeft depuis BottomRight")

    def topRight(self):
        self._transition(TopRight)

    def bottomLeft(self):
        self._transition(BottomLeft)

    def bottomRight(self):
        print("le joueur est déjà en BottomRight")


