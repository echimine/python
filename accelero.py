
import math
window = None
document= None
create_proxy = None

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

class AccelSensor(Smartphone):
    def __init__(self):
        self.smartfone = Smartphone()

    def get_xyz(self):
        xyz = window.getAccelXYZ()
        x = float(xyz[0] or 0.0)
        y = float(xyz[1] or 0.0)
        z = float(xyz[2] or 0.0)
        return x, y, z

    def get_magnitude(self):
        x, y, z = self.get_xyz()
        return math.sqrt(x*x + y*y + z*z)
    
    def get_state(self, x, y, z):
        if y>7:
            self.smartfone.to_up()
            return self.smartfone.state.name
        if y<-7:
           self.smartfone.to_down()
           return self.smartfone.state.name
        if x>7:
           self.smartfone.to_left()
           return self.smartfone.state.name
        if x<-7:
            self.smartfone.to_right()
            return self.smartfone.state.name


accel = AccelSensor()
def update(*args, **kwargs):
    x, y, z = accel.get_xyz()
    result = accel.get_state(x=x,y=y,z=z)
    m = accel.get_magnitude()
    document.getElementById("values").innerText = (
        f"x={x:.2f}, y={y:.2f}, z={z:.2f}, |a|={m:.2f}, state={result}"
    )
    window.addAccelPoint(x, y, z)

update_proxy = create_proxy(update)
window.setInterval(update_proxy, 200)