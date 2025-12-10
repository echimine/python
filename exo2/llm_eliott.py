from client_llamacpp import send_llama_chat
from abc import ABC, abstractmethod


class WeatherState(ABC):
    def __init__(self, weatherState):
        self.weatherState = weatherState

    def on_enter(self, from_state: "WeatherState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "WeatherState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    # Weather 1|0
    @abstractmethod
    def no_located_found(self):
        pass

    @abstractmethod
    def located_found(self):
        pass

    @abstractmethod
    def no_date_found(self):
        pass

    @abstractmethod
    def date_found(self):
        pass

     # utilitaire
    def _transition(self, new_state_cls: type["WeatherState"], ):
        self.weatherState.set_weather_state(new_state_cls)

class LocatedFoundState(WeatherState):
    @property
    def name(self) -> str:
        return "LocatedFound"
        
    def no_located_found(self):
        self._transition(NoLocatedFound)

    def located_found(self):
        print("pas de transition possible tu es déjà en locatedFound")

    def no_date_found(self):
        self._transition(DateMissing)

    def date_found(self):
        print("pas de transition possible tu es déjà en dateFound")

class NoLocatedFound(WeatherState):
    @property
    def name(self) -> str:
        return "NoLocatedFound"
        
    def no_located_found(self):
        print("pas de transition possible tu es déjà en noLocatedFound")

    def located_found(self):
        self._transition(LocatedFoundState)

    def no_date_found(self):
        self._transition(DateMissing)

    def date_found(self):
        print("pas de transition possible tu es déjà en dateFound")

class DateMissing(WeatherState):
    @property
    def name(self) -> str:
        return "DateMissing"
        
    def no_located_found(self):
        self._transition(NoLocatedFound)

    def located_found(self):
        self._transition(LocatedFoundState)

    def no_date_found(self):
        print("pas de transition possible tu es déjà en dateMissing")

    def date_found(self):
        self._transition(LocatedFoundState)

class DateFound(WeatherState):
    @property
    def name(self) -> str:
        return "DateFound"
        
    def no_located_found(self):
        self._transition(NoLocatedFound)

    def located_found(self):
        self._transition(LocatedFoundState)

    def no_date_found(self):
        self._transition(DateMissing)

    def date_found(self):
        print("pas de transition possible tu es déjà en dateFound")

class Weather:
    def __init__(self):
        # 1 — état localisation
        self.location_state: WeatherState = NoLocatedFound(self)
        self.location_state.on_enter(None)

        # 2 — état date
        self.date_state: WeatherState = DateMissing(self)
        self.date_state.on_enter(None)

    def set_location_state(self, new_state_cls):
        old_state = self.location_state
        new_state = new_state_cls(self)
        old_state.on_exit(new_state)
        new_state.on_enter(old_state)
        self.location_state = new_state

    def set_weather_state(self, new_state_cls):
        """Router helper: route a generic state class to the correct
        location vs date setter so WeatherState._transition can call a
        single method.
        """
        # location states
        location_states = (LocatedFoundState, NoLocatedFound)
        # date states
        date_states = (DateMissing, DateFound)

        if issubclass(new_state_cls, location_states):
            self.set_location_state(new_state_cls)
        elif issubclass(new_state_cls, date_states):
            self.set_date_state(new_state_cls)
        else:
            raise ValueError(f"Unknown routed state class: {new_state_cls}")

    def set_date_state(self, new_state_cls):
        old_state = self.date_state
        new_state = new_state_cls(self)
        old_state.on_exit(new_state)
        new_state.on_enter(old_state)
        self.date_state = new_state

answer = send_llama_chat(system_prompt="""Tu dois déterminer si tu dispose des de toutes les informations nécessaires pour répondre à la question.
Si la question correspond à une demande de météo en fonction d'une ville et d'une date.
Tu analyses si tu as toutes les informations nécessaires (ville et date).
Tu réponds de la manière suivante:
```
{
    "has_date" : true or false,
    "has_city" : true or false
}
```                 
""",
                        user_content="""
                        Yo! il fait quel temps à Annecy ?
                        """)

start = answer.find("```")
end = answer.find("```", start + 3)
if start != -1 and end != -1:
    current_state = answer[start + 3:end].strip()
else:
    current_state = answer.strip()
print("Current state extracted:\n", current_state)
# extract values from the json-like response 
import json
state_dict = json.loads(current_state)
has_date = state_dict.get("has_date", False)
has_city = state_dict.get("has_city", False)    
print(f"has_date: {has_date}, has_city: {has_city}")

weather = Weather()

if has_city:
    weather.location_state.located_found()
else:
    weather.location_state.no_located_found()

if has_date:
    weather.date_state.date_found()
else:
    weather.date_state.no_date_found()








































# answer = send_llama_chat(system_prompt="""Si on te demande la météo pour une ville, tu réponds:
#                         ```get_weather("nom_de_la_ville", date)```
# Si tu as besoin de connaitre la date actuelle, tu réponds:
#                         ```get_current_date()```
                         
# Etapes à suivre:
# Soit il te manque des informations pour répondre à la question, soit tu disposes de toutes les informations nécessaires.
                         
# # CAS INFORMATIONS MANQUANTES:
#     1. Si la date actuelle est nécessaire, utilise get_current_date() pour l'obtenir.
#     2. Utilise la date obtenue pour formuler la requête météo avec get_weather("nom_de_la_ville", date).
# # CAS INFORMATIONS DISPONIBLES:
#     1. Fournis la réponse directement sans appeler de fonction.
                         
#                         """,
#                         user_content="""
#                         Yo! il fait quel temps à Annecy aujourd'hui?
#                         """)



# print(answer)
# # Extract the function call from the answer
# start = answer.find("```")
# end = answer.find("```", start + 3)
# if start != -1 and end != -1:
#     function_call = answer[start + 3:end].strip()
#     print("Function call extracted:", function_call)