from movementState import (
    MouvementState,
    StaticState,
)

from playingState import (
    PlaybleState,
    Playble,
)

from positionnedState import (
    PositionnedState,
    BottomLeft
)
from abc import ABC, abstractmethod


class HeroState(ABC,):
    def __init__(self, heroState,):
        self.heroState = heroState
        

    def on_enter(self, from_state: "HeroState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "HeroState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass


    @abstractmethod
    def isPlayingGame(self):
        pass

    @abstractmethod
    def isNotPlayingGame(self):
        pass
    
    # utilitaire
    def _transition(self, new_state_cls: type["PositionnedState"], ):
        self.heroState.set_positionned_state(new_state_cls)


class IsPlayingGame(HeroState):
    @property
    def name(self) -> str:
        return "IsPlayingGame"
        
    def isPlayingGame(self):
        print("le joueur est déjà en Playble")

    def isNotPlayingGame(self):
        print("pas possible")

class IsNotPlayingGame(HeroState):
    @property
    def name(self) -> str:
        return "IsNotPlayingGame"
        
    def isPlayingGame(self):
        print("pas possible de transiter vers playing")

    def isNotPlayingGame(self):
        print("cannot played because end game")











class Hero:
    def __init__(self):
        self.hero_state: HeroState
        self.moving_state: MouvementState = StaticState(self)
        self.playble_state: PlaybleState = Playble(self)
        self.positionned_state : PositionnedState = BottomLeft(self)

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
