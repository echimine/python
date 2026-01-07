# Configuration de l'Assistant

Ce projet nécessite la configuration de variables d'environnement pour fonctionner correctement, notamment pour l'accès à Gmail.

Mettez-vous dans le dossier tp_final.

## 1. Création du fichier `.env`

Créez un fichier nommé `.env` à la racine de votre projet (dans le même dossier que `examples_agent.py` ou à la racine de votre workspace).

Ce fichier doit contenir les informations suivantes :

```env
GMAIL_EMAIL=votre_email@gmail.com
GMAIL_PASSWORD=votre_mot_de_passe_application
```

## 2. Générer un Mot de passe d'application Google

**Attention :** Vous ne devez pas utiliser votre mot de passe Gmail habituel. Il faut générer un mot de passe spécifique pour cette application.

**Pré-requis sur Google** : La validation en deux étapes (2FA) doit souvent être activée pour avoir accès aux mots de passe d'application.

### Étapes sur Google Chrome :

1.  Accédez à votre compte Google : [https://myaccount.google.com/](https://myaccount.google.com/)
2.  Dans le menu de gauche, cliquez sur **Sécurité**.
3.  Cherchez la section **Comment vous connecter à Google**.
4.  Cliquez sur **Validation en deux étapes** (si ce n'est pas déjà activé, activez-le).
5.  Une fois dans la validation en deux étapes (ou en revenant dans le menu Sécurité), cherchez **Mots de passe des applications** (souvent tout en bas de la page).
    *   *Note : Vous pouvez aussi chercher "Mots de passe des applications" dans la barre de recherche en haut.*
6.  Donnez un nom à l'application (ex: `PythonAgent`) et cliquez sur **Créer**.
7.  Google va afficher une fenêtre jaune avec un code de 16 lettres (ex: `abcd efgh ijkl mnop`).
8.  **Copiez ce code.**
9.  Collez-le dans votre fichier `.env` pour la variable `GMAIL_PASSWORD` (vous pouvez le coller avec ou sans espaces).

## 3. Lancer l'agent

Une fois le fichier `.env` configuré :

```bash
python examples_agent.py
```
