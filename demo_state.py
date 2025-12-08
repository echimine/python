from abc import ABC, abstractmethod

class SmartphoneState(ABC):

    def __init__(self, phone):
        self.phone = phone

    def on_enter(self, from_state: "SmartphoneState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "SmartphoneState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def to_left(self):
        pass

    @abstractmethod
    def to_right(self):
        pass
    
    @abstractmethod
    def to_up(self):
        pass
    
    @abstractmethod
    def to_down(self):
        pass

     # utilitaire
    def _transition(self, new_state_cls: type["SmartphoneState"], ):
        self.phone.set_state(new_state_cls)


class UpState(SmartphoneState):

    @property
    def name(self) -> str:
        return "UP"
    
    def to_up(self):
        # déjà en UP
        print("Déjà en UP, aucune transition.")

    def to_down(self):
        print("Transition invalide : UP -> DOWN")

    def to_left(self):
        self._transition(LeftState)

    def to_right(self):
        self._transition(RightState)


class LeftState(SmartphoneState):

    @property
    def name(self) -> str:
        return "LEFT"
    
    def to_up(self):
        # déjà en UP
        self._transition(UpState)

    def to_down(self):
        self._transition(DownState)

    def to_left(self):
        print("Déjà en LEFT, aucune transition.")

    def to_right(self):
        print("Transition invalide : LEFT -> RIGHT")

class RightState(SmartphoneState):
     
    @property
    def name(self) -> str:
        return "RIGHT"
    
    def to_up(self):
        # déjà en UP
        self._transition(UpState)

    def to_down(self):
        self._transition(DownState)

    def to_left(self):
        print("Transition invalide : RIGHT -> LEFT")

    def to_right(self):
        print("Déjà en RIGHT, aucune transition.")

class DownState(SmartphoneState):

    @property
    def name(self) -> str:
        return "DOWN"
    
    def to_up(self):
        # déjà en UP
        print("Transition invalide : DOWN -> UP")

    def to_down(self):
        print("Déjà en DOWN, aucune transition.")

    def to_left(self):
        self._transition(LeftState)

    def to_right(self):
        self._transition(RightState)


class Smartphone:

    def __init__(self, callback=None):
        self.update_ui = callback or (lambda state_name: None)
        self.state: SmartphoneState = UpState(self)
        # entrée initiale
        self.state.on_enter(None)
        self.update_ui(self.state.name)

    def set_state(self, new_state_cls: type["SmartphoneState"]):
        old_state = self.state
        new_state = new_state_cls(self)

        # Hooks de sortie / entrée
        old_state.on_exit(new_state)
       
        new_state.on_enter(old_state)

        self.state = new_state
        self.update_ui(self.state.name)

    # Récupération des données d'accélération
    

    # API publique : on déclenche des événements, pas des états bruts
    def to_up(self):
        self.state.to_up()

    def to_down(self):
        self.state.to_down()

    def to_left(self):
        self.state.to_left()

    def to_right(self):
        self.state.to_right()



if __name__ == "__main__":
    phone = Smartphone()

    print("\n--- UP -> LEFT ---")
    phone.to_left()

    print("\n--- LEFT -> UP ---")
    phone.to_up()

    print("\n--- UP -> RIGHT ---")
    phone.to_right()

    print("\n--- RIGHT -> DOWN ---")
    phone.to_down()

    print("\n--- DOWN -> UP (invalide) ---")
    phone.to_up()
