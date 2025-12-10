# from movementState import (
#     MouvementState,
#     StaticState,
# )

# from playingState import (
#     PlaybleState,
#     Playble,
# )

from positionnedState import (
    PositionnedState,
    BottomLeft
)
from abc import ABC, abstractmethod


class HeroState(ABC):

    def __init__(self, hero):
        self.hero = hero

    def on_enter(self, from_state: "HeroState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "HeroState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

     # utilitaire
    def _transition(self, new_state_cls: type["HeroState"], ):
        self.hero.set_state(new_state_cls)

    def to_movement(self):
        pass

    def to_stationary(self):
        pass

    def to_finished(self):
        pass

class MovingHeroState(HeroState):
    @property
    def name(self) -> str:
        return "MOVING"
    

    def on_enter(self, from_state: "HeroState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "HeroState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")
    


    def to_movement(self):
        # déjà en MOVING
        print("Déjà en MOVING, aucune transition.")

    def to_stationary(self):
        self._transition(StationaryHeroState)

    def to_finished(self):
        self._transition(FinishedHeroState)


class StationaryHeroState(HeroState):

    @property
    def name(self) -> str:
        return "STATIONARY"
    
    def to_stationary(self):
        # déjà en STATIONARY
        print("Déjà en STATIONARY, aucune transition.")

    def to_movement(self):
        self._transition(MovingHeroState)

    def to_finished(self):
        self._transition(FinishedHeroState)

class FinishedHeroState(HeroState):

    @property
    def name(self) -> str:
        return "FINISHED"
    
    def to_finished(self):
        # déjà en FINISHED
        print("Déjà en FINISHED, aucune transition.")

    def to_movement(self):
         print("Déjà en FINISHED, aucune transition.")

    def to_stationary(self):
         print("Déjà en FINISHED, aucune transition.")



class Hero:
    def __init__(self, game_widget):
        self.game_widget = game_widget
        self.hero_state:HeroState = StationaryHeroState(self)
        self.hero_state.on_enter(None)
        self.hero_position_state:PositionnedState = BottomLeft(self)

    # Modifier set_state ou créer une nouvelle méthode, pour gérer les 3 types d'état
    def set_state(self, new_state_cls, action=None):
        old_state = self.hero_state
        new_state = new_state_cls(self)
        # Hooks de sortie / entrée
        old_state.on_exit(new_state)
        new_state.on_enter(old_state)
        self.hero_state = new_state

    def set_position(self, new_state_cls):
        old_state = self.hero_position_state
        


# hero = Hero()
# hero.moving_state.move()
# hero.moving_state.static()
# hero.positionned_state.topLeft()
# hero.positionned_state.bottomRight()
# hero.playble_state.notPlayble()
