from abc import ABC, abstractmethod
class DateState(ABC):
    def __init__(self, playbleState):
        self.playbleState = playbleState

    def on_enter(self, from_state: "DateState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "DateState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    # Date 1|0
    @abstractmethod
    def is_date(self):
        pass

    @abstractmethod
    def no_date(self):
        pass

     # utilitaire
    def _transition(self, new_state_cls: type["DateState"], ):
        self.playbleState.set_date_state(new_state_cls)



class IsDate(DateState):
    @property
    def name(self) -> str:
        return "IsDate"
        
    def is_date(self):
        print("pas de transition il y a déjà la date")

    def no_date(self):
        self._transition(NoDate)

class NoDate(DateState):
    @property
    def name(self) -> str:
        return "NoDate"
        
    def is_date(self):
        print(IsDate)

    def no_date(self):
        print("pas de transition possible tu es déjà en noDate")

