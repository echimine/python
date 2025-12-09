# State Pattern

"Représente des relations entre les états": 
une relation == action/evenement/changement 

### Methode de construction:

1) Déterminer la liste des états du systeme

2) Déterminer la liste des relations (actions/evenement/changement) entre les états

3) Mettre en relation les états (a partir de la liste)

4) Etudier la dynamique

### Methode de réalisation:
##### Outils nécessaires pour la création d'un état abstrait/générique à notre systeme:
1) Classe Abstraite / Protocole / Interface représentant un état générique.

2) Définir des fonctions de log (on_enter/on_exit) (connaitre le fait qu'on entre ou qu'on sort de l'état)

3) Définir les méthodes correspondant a l'ensemble des transitions/relations.

4) Définir la méthode implémentant la mécanique de transition.

##### Concrétisation / Spécialisation:
Chaque état identifié par la méthode de construction doit être implémenté.

Chaque état hérite de la classe réprésentant l'état abstrait / générique.
On spécifie l'état générique.

1) On hérite de la classe abstraite.

2) On implémente les relations spécifique à l'état implémenté.

##### Intégrer la machine a état dans son contexte d'execution
Le contexte d'execution c'est le systeme dont les état représente les différentes situations auquel il peut être confronté.






