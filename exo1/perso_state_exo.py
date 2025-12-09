# implémentation de la class abstraite
from abc import ABC, abstractmethod
class MouvementState(ABC):
    def __init__(self, mouvementState):
        self.mouvementState = mouvementState

    def on_enter(self, from_state: "MouvementState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "MouvementState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    # MOUVEMENT 1|0
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def static(self):
        pass
    
     # utilitaire
    def _transition(self, new_state_cls: type["MouvementState"], ):
        self.mouvementState.set_moving_state(new_state_cls)

class MovingSate(MouvementState):
    @property
    def name(self) -> str:
        return "MovingSate"
        
    def move(self):
        print("le joueur ne peut pas changer de direction car il est déjà en train de bouger")

    def static(self):
        self._transition(StaticState)
    
class StaticState(MouvementState):
    @property
    def name(self) -> str:
        return "StaticState"
        
    def move(self):
        self._transition(MovingSate)

    def static(self):
        print("le joueur est déjà en static")


class PositionnedState:
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


class PlaybleState:
    def __init__(self, playbleState):
        self.playbleState = playbleState

    def on_enter(self, from_state: "PlaybleState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "PlaybleState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    # MOUVEMENT 1|0
    @abstractmethod
    def playble(self):
        pass

    @abstractmethod
    def notPlayble(self):
        pass

     # utilitaire
    def _transition(self, new_state_cls: type["PlaybleState"], ):
        self.playbleState.set_playing_state(new_state_cls)

class Playble(PlaybleState):
    @property
    def name(self) -> str:
        return "Playble"
        
    def playble(self):
        print("le joueur est déjà en Playble")

    def notPlayble(self):
        self._transition(NotPlayble)

class NotPlayble(PlaybleState):
    @property
    def name(self) -> str:
        return "NotPlayble"
        
    def playble(self):
        print("le jeu est fini on ne peut pas revenir à playable")

    def notPlayble(self):
        print("le joueur est déjà en NotPlayble")


class Hero:
    def __init__(self):
        self.moving_state: MouvementState = StaticState(self)
        self.moving_state.on_enter(None)
        self.playble_state: PlaybleState = Playble(self)
        self.playble_state.on_enter(None)
        self.positionned_state : PositionnedState = BottomLeft(self)
        self.positionned_state.on_enter(None)

    def set_moving_state(self, new_state_cls: type["MouvementState"]):
        old_state = self.moving_state
        new_state = new_state_cls(self)
        old_state.on_exit(new_state)
        new_state.on_enter(old_state)
        self.moving_state = new_state
    def set_playing_state(self, new_state_cls: type["PlaybleState"]):
        old_state = self.playble_state
        new_state = new_state_cls(self)
        old_state.on_exit(new_state)
        new_state.on_enter(old_state)
        self.playble_state = new_state

    def set_positionned_state(self, new_state_cls: type["PositionnedState"]):
        old_state = self.positionned_state
        new_state = new_state_cls(self)
        old_state.on_exit(new_state)
        new_state.on_enter(old_state)
        self.positionned_state = new_state


hero = Hero()
hero.moving_state.move()
hero.moving_state.static()
hero.positionned_state.topLeft()
hero.positionned_state.bottomRight()
hero.playble_state.notPlayble()
