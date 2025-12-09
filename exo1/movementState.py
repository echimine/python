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


