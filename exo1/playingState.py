from abc import ABC, abstractmethod
class PlaybleState(ABC):
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
