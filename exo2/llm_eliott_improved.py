from client_llamacpp import send_llama_chat
from abc import ABC, abstractmethod
import json

# ============================================================
# MACHINE À ÉTAT 1: DateState (Date présente ou absente)
# ============================================================

class DateState(ABC):
    def __init__(self, context):
        self.context = context  # ← Référence au contexte global

    def on_enter(self, from_state: "DateState | None"):
        print(f"[ENTER DATE] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "DateState"):
        print(f"[EXIT DATE]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def set_date_found(self):
        pass

    @abstractmethod
    def set_date_not_found(self):
        pass

    def _transition(self, new_state_cls: type["DateState"]):
        old_state = self.context.date_state
        new_state = new_state_cls(self.context)
        old_state.on_exit(new_state)
        new_state.on_enter(old_state)
        self.context.date_state = new_state


class IsDate(DateState):
    @property
    def name(self) -> str:
        return "IsDate"
        
    def set_date_found(self):
        print("✓ Déjà en IsDate")

    def set_date_not_found(self):
        self._transition(NoDate)


class NoDate(DateState):
    @property
    def name(self) -> str:
        return "NoDate"
        
    def set_date_found(self):
        self._transition(IsDate)

    def set_date_not_found(self):
        print("✓ Déjà en NoDate")


# ============================================================
# MACHINE À ÉTAT 2: LocateState (Localisation présente ou absente)
# ============================================================

class LocateState(ABC):
    def __init__(self, context):
        self.context = context

    def on_enter(self, from_state: "LocateState | None"):
        print(f"[ENTER LOCATE] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "LocateState"):
        print(f"[EXIT LOCATE]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def set_location_found(self):
        pass

    @abstractmethod
    def set_location_not_found(self):
        pass

    def _transition(self, new_state_cls: type["LocateState"]):
        old_state = self.context.locate_state
        new_state = new_state_cls(self.context)
        old_state.on_exit(new_state)
        new_state.on_enter(old_state)
        self.context.locate_state = new_state


class IsLocated(LocateState):
    @property
    def name(self) -> str:
        return "IsLocated"
        
    def set_location_found(self):
        print("✓ Déjà en IsLocated")

    def set_location_not_found(self):
        print("✗ Pas de transition depuis IsLocated")


class NoLocated(LocateState):
    @property
    def name(self) -> str:
        return "NoLocated"
        
    def set_location_found(self):
        self._transition(IsLocated)

    def set_location_not_found(self):
        print("✓ Déjà en NoLocated")


# ============================================================
# CONTEXTE: gère les deux machines à état
# ============================================================

class WeatherContext:
    """Contexte pour gérer la requête météo"""
    def __init__(self):
        self.date_state: DateState = NoDate(self)
        self.date_state.on_enter(None)
        
        self.locate_state: LocateState = NoLocated(self)
        self.locate_state.on_enter(None)
    
    def process_query(self, user_query: str):
        """Traite une requête météo"""
        print(f"\n📝 Traitement: {user_query}\n")
        
        # Appeler le LLM
        answer = send_llama_chat(
            system_prompt="""Tu dois déterminer si tu disposes de toutes les informations nécessaires.
Si la question correspond à une demande de météo (ville + date).
Réponds ainsi:
```
{
    "has_date" : true or false,
    "has_city" : true or false
}
```""",
            user_content=user_query
        )
        
        # Parser la réponse
        start = answer.find("```")
        end = answer.find("```", start + 3)
        if start != -1 and end != -1:
            json_str = answer[start + 3:end].strip()
        else:
            json_str = answer.strip()
        
        state_dict = json.loads(json_str)
        has_date = state_dict.get("has_date", False)
        has_city = state_dict.get("has_city", False)
        
        print(f"✓ has_date: {has_date}, has_city: {has_city}\n")
        
        # Mettre à jour les deux machines à état
        if has_date:
            self.date_state.set_date_found()
        else:
            self.date_state.set_date_not_found()
        
        if has_city:
            self.locate_state.set_location_found()
        else:
            self.locate_state.set_location_not_found()
        
        print(f"\n📊 État final: {self.date_state.name} + {self.locate_state.name}\n")
        
        # Décider l'action
        self._decide_action()
    
    def _decide_action(self):
        """Décide quoi faire en fonction des états"""
        date = self.date_state.name
        locate = self.locate_state.name
        
        if date == "IsDate" and locate == "IsLocated":
            print("🎯 Action: Récupérer la météo")
        elif date == "NoDate" and locate == "IsLocated":
            print("⚠️  Action: Demander la date")
        elif date == "IsDate" and locate == "NoLocated":
            print("⚠️  Action: Demander la localisation")
        else:
            print("⚠️  Action: Demander date ET localisation")


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    context = WeatherContext()
    # Test simple
    context.process_query("Yo! il fait quel temps à Annecy ?")
