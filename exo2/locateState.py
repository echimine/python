from abc import ABC, abstractmethod
class LocateState(ABC):
    def __init__(self, playbleState):
        self.playbleState = playbleState

    def on_enter(self, from_state: "LocateState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "LocateState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    # Date 1|0
    @abstractmethod
    def is_located(self):
        pass

    @abstractmethod
    def no_located(self):
        pass

     # utilitaire
    def _transition(self, new_state_cls: type["LocateState"], ):
        self.playbleState.set_location_state(new_state_cls)



class isLocated(LocateState):
    @property
    def name(self) -> str:
        return "isLocated"
        
    def is_located(self):
        print("pas de transition il y a déjà la date")

    def no_located(self):
        self._transition(noLocated)

class noLocated(LocateState):
    @property
    def name(self) -> str:
        return "noLocated"
        
    def is_located(self):
        print(isLocated)

    def no_located(self):
        print("pas de transition possible tu es déjà en noLocated")

