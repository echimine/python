
# =========================
# Handlers d'exemple
# =========================
import pygame
from typing import Any, Dict
from agent import MultiSkillAgent, Skill, Slot, send_llama_chat, parse_json_loose
from pathlib import Path
from typing import Dict
import pygame
import time
import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
from icalendar import Calendar, Event
from datetime import datetime
import dateparser
import uuid

load_dotenv()

uuidee = uuid.uuid4()

BASE_DIR = Path(__file__).resolve().parent
MUSIC_PATH = BASE_DIR / "music" / "get_back.wav"


def get_safe_filename(title: str) -> str:
    """Génère un nom de fichier sûr à partir d'un titre."""
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
    return f"{safe_title}.ics"

def get_event_filepath(title: str) -> Path:
    """Retourne le chemin complet du fichier événement."""
    filename = get_safe_filename(title)
    return BASE_DIR / filename

def agenda_on_ready(values: Dict[str, str]) -> str:
    title = values.get("titre", "un événement")
    start_str = values.get("date de début", "demain 10h")
    end_str = values.get("date de fin", "demain 11h")

    dt_start = dateparser.parse(start_str)
    dt_end = dateparser.parse(end_str)

    if not dt_start:
        dt_start = datetime.now()
    if not dt_end:
        dt_end = datetime.now()

    cal = Calendar()
    cal.add("prodid", "-//Projet IA Locale//Calendar Assistant")
    cal.add("version", "2.0")

    event = Event()
    event.add("uid", f"{uuid.uuid4()}@ia")
    event.add("summary", title)
    event.add("dtstart", dt_start)
    event.add("dtend", dt_end)
    event.add("description", f"Événement : {title}")

    cal.add_component(event)

    filename = get_safe_filename(title)
    
    with open(filename, "wb") as f:
        f.write(cal.to_ical())

    return (
        f"L'événement '{title}' a été créé dans le fichier {filename} "
        f"(du {dt_start} au {dt_end})."
    )

def delete_agenda_on_ready(values: Dict[str, str]) -> str:
    title = values.get("titre", "un événement")
    filepath = get_event_filepath(title)
    
    if filepath.exists():
        filepath.unlink()
        return f"L'événement '{title}' (fichier {filepath.name}) a été supprimé."
    else:
        return f"Je n'ai pas trouvé d'événement intitulé '{title}' (fichier {filepath.name} inexistant)."

def modify_agenda_on_ready(values: Dict[str, str]) -> str:
    title = values.get("titre", "")
    instructions = values.get("instructions", "")
    
    filepath = get_event_filepath(title)
    
    if not filepath.exists():
        return f"Je ne trouve pas l'événement '{title}' à modifier."
        
    with open(filepath, "rb") as f:
        cal = Calendar.from_ical(f.read())
        
    event_component = None
    for component in cal.walk():
        if component.name == "VEVENT":
            event_component = component
            break
            
    if not event_component:
        return f"Le fichier {filepath.name} ne contient pas d'événement valide."
        
    current_summary = str(event_component.get("summary"))
    current_dtstart = event_component.get("dtstart").dt
    current_dtend = event_component.get("dtend").dt
    
    system_prompt = f"""
Tu es un assistant expert en modification d'agenda.
Voici l'événement actuel :
- Titre : "{current_summary}"
- Début : {current_dtstart}
- Fin : {current_dtend}

L'utilisateur veut : "{instructions}"

Tu dois retourner les NOUVELLES valeurs. Si une valeur ne change pas, renvoie la même.
Format JSON attendu :
{{
  "new_title": "...",
  "new_start": "YYYY-MM-DD HH:MM:SS",
  "new_end": "YYYY-MM-DD HH:MM:SS"
}}
"""
    response_json = send_llama_chat(
        system_prompt=system_prompt,
        user_content="Applique les changements demandés.",
        temperature=0.0
    )
    
    data = parse_json_loose(response_json)
    
    new_title = data.get("new_title", current_summary)
    new_start_str = data.get("new_start")
    new_end_str = data.get("new_end")
    
    # Parsing dates
    new_dtstart = dateparser.parse(new_start_str) if new_start_str else current_dtstart
    new_dtend = dateparser.parse(new_end_str) if new_end_str else current_dtend
    
    if not new_dtstart: new_dtstart = current_dtstart
    if not new_dtend: new_dtend = current_dtend
    
    # Mise à jour
    # Si le titre change, on supprime l'ancien fichier et on en crée un nouveau
    if new_title != current_summary:
        filepath.unlink()
        new_filepath = get_event_filepath(new_title)
    else:
        new_filepath = filepath
        
    # Recréation propre pour éviter les artefacts
    new_cal = Calendar()
    new_cal.add("prodid", "-//Projet IA Locale//Calendar Assistant")
    new_cal.add("version", "2.0")
    
    new_event = Event()
    new_event.add("uid", f"{uuid.uuid4()}@ia")
    new_event.add("summary", new_title)
    new_event.add("dtstart", new_dtstart)
    new_event.add("dtend", new_dtend)
    new_event.add("description", f"Événement : {new_title}")
    
    new_cal.add_component(new_event)
    
    with open(new_filepath, "wb") as f:
        f.write(new_cal.to_ical())
        
    return f"L'événement a été modifié.\nNouveau titre : {new_title}\nDébut : {new_dtstart}\nFin : {new_dtend}"


    with open(new_filepath, "wb") as f:
        f.write(new_cal.to_ical())
        
    return f"L'événement a été modifié.\nNouveau titre : {new_title}\nDébut : {new_dtstart}\nFin : {new_dtend}"

def fetch_recent_emails(username, password, limit=5):
    """Récupère les N derniers emails via IMAP."""
    try:
        # Connexion au serveur IMAP de Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")

        # Recherche des derniers emails
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            return []

        email_ids = messages[0].split()
        latest_email_ids = email_ids[-limit:]
        
        emails_data = []

        for e_id in reversed(latest_email_ids):
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            if status != "OK":
                continue
                
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Décodage du sujet
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                        
                    # Décodage de l'expéditeur
                    sender = msg.get("From")
                    
                    # Récupération du corps (texte brut préféré)
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            
                            if "attachment" not in content_disposition:
                                payload = part.get_payload(decode=True)
                                if payload:
                                    charset = part.get_content_charset() or "utf-8"
                                    try:
                                        decoded_payload = payload.decode(charset, errors="replace")
                                    except (LookupError, AttributeError):
                                        decoded_payload = payload.decode("utf-8", errors="replace")
                                else:
                                    decoded_payload = ""

                                if content_type == "text/plain":
                                    body = decoded_payload
                                    break # On préfère le text/plain
                                elif content_type == "text/html" and not body:
                                    body = decoded_payload
                    else:
                        payload = msg.get_payload(decode=True)
                        if payload:
                            charset = msg.get_content_charset() or "utf-8"
                            try:
                                body = payload.decode(charset, errors="replace")
                            except (LookupError, AttributeError):
                                body = payload.decode("utf-8", errors="replace")
                        else:
                            body = ""
                        
                    emails_data.append({
                        "sender": sender,
                        "subject": subject,
                        "body": body[:500] + "..." if len(body) > 500 else body # Tronquer pour le LLM
                    })
                    
        mail.close()
        mail.logout()
        return emails_data
        
    except Exception as e:
        print(f"Erreur IMAP: {e}")
        return []

def email_summary_on_ready(values: Dict[str, str]) -> str:
    count_str = values.get("count", "5")
    try:
        limit = int(count_str)
    except ValueError:
        limit = 5
        
    username = os.environ.get("GMAIL_EMAIL")
    password = os.environ.get("GMAIL_PASSWORD")
    
    if not username or not password:
        return "Je ne peux pas récupérer vos emails car les variables d'environnement GMAIL_EMAIL et GMAIL_PASSWORD ne sont pas définies."
        
    emails = fetch_recent_emails(username, password, limit)
    
    if not emails:
        return "Je n'ai trouvé aucun email récent ou je n'ai pas pu me connecter."
        
    # Construction du prompt pour le LLM
    emails_text = ""
    for i, em in enumerate(emails, 1):
        emails_text += f"Email {i}:\nDe: {em['sender']}\nSujet: {em['subject']}\nCorps: {em['body']}\n\n"
        
    system_prompt = """
Tu es un assistant personnel efficace.
Tu reçois une liste d'emails récents.
Tu dois en faire une synthèse claire et concise en français.
Pour chaque email important, résume en une phrase. Ignore les publicités évidentes si possible.
"""
    summary = send_llama_chat(
        system_prompt=system_prompt,
        user_content=f"Voici mes derniers emails :\n{emails_text}",
        temperature=0.7
    )
    
    return f"Voici la synthèse de vos {len(emails)} derniers emails :\n\n{summary}"

def music_on_ready(values: Dict[str, str]) -> str:
    name = values.get("music", "une musique inconnue")

    if not MUSIC_PATH.exists():
        return f"Erreur : fichier audio introuvable ({MUSIC_PATH})"

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.load(str(MUSIC_PATH))
    pygame.mixer.music.play()

    # Attente non bloquante
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    return f"La musique {name} est en cours de lecture"


def write_txt_file_on_ready(values: Dict[str, str]) -> str:
    file = values.get("name", "un fichier")
    content = values.get("content", "")
    with open(f"{file}.txt", "w") as f:
        f.write(content)
    return f"Le contenu a été écrit dans le fichier {file}."


def read_txt_file_on_ready(values: Dict[str, str]) -> str:
    file = values.get("file_path", "un fichier")
    try:
        with open(file, "r") as f:
            content = f.read()
        return f"Contenu du fichier {file}:\n{content}"
    except FileNotFoundError:
        return f"Le fichier {file} n'existe pas."


def weather_on_ready(values: Dict[str, str]) -> Dict[str, Any]:
    city = values.get("city")
    date = values.get("date")

    return {
        "type": "weather_result",
        "city": city,
        "date": date,
        "forecast": {
            "summary": "ensoleillé avec quelques nuages",
            "temperature_min": 5,
            "temperature_max": 14,
        },
        "note": "Les données météo sont fictives dans cet exemple.",
    }


def booking_on_ready(values: Dict[str, str]) -> str:
    restaurant = values.get("restaurant_name", "un restaurant")
    date = values.get("date", "une date inconnue")
    time = values.get("time", "une heure inconnue")
    people = values.get("people", "un certain nombre de")

    return (
        f"Parfait ! Je récapitule : réservation à {restaurant}, "
        f"le {date} à {time}, pour {people} personnes. "
        f"(Je ne fais pas la réservation réelle, c'est un exemple.)"
    )


# =========================
# Construction de l'agent
# =========================

def build_agent() -> MultiSkillAgent:

    agenda_slots = [
        Slot(
            name="date de début",
            description="date de début de l'événement",
            question="quelle est la date du début de l'événement",
        ),

        Slot(
            name="date de fin",
            description="date de fin de l'événement",
            question="quelle est la date de fin de l'événement",
        ),

        Slot(
            name="titre",
            description="le titre de l'événement",
            question="quel est le titre de l'événement",
        )

    ]

    agenda_skills = Skill(
        name="agenda",
        description="création d'un événement dans l'agenda",
        slots=agenda_slots,
        final_answer_system_prompt="""
Tu es un assistant qui créer un fichier .ics pour écrire, modifier ou supprimer des évenements.
Tu reçois des données structurées, tu receveras :
- une date de début,
- une date de fin d'évenement,
- un titre d'évenement.
exemple de phrase : "ajoute un rendez-vous pour le 15 juin 2024 de 14h à 15h intitulé réunion projet"
""",
        on_ready=agenda_on_ready,
    )

    delete_agenda_slots = [
        Slot(
            name="titre",
            description="le titre de l'événement à supprimer",
            question="quel est le titre de l'événement à supprimer",
        )
    ]

    delete_agenda_skill = Skill(
        name="delete_agenda",
        description="supprimer un événement de l'agenda",
        slots=delete_agenda_slots,
        final_answer_system_prompt="""
Tu es un assistant qui supprime des événements.
Tu as reçu le titre de l'événement à supprimer.
""",
        on_ready=delete_agenda_on_ready,
    )

    modify_agenda_slots = [
        Slot(
            name="titre",
            description="le titre de l'événement à modifier",
            question="quel est le titre de l'événement à modifier",
        ),
        Slot(
            name="instructions",
            description="les instructions de modification (ex: changer la date, changer le titre)",
            question="quelles sont les modifications à apporter ?",
        )
    ]

    modify_agenda_skill = Skill(
        name="modify_agenda",
        description="modifier un événement de l'agenda existant",
        slots=modify_agenda_slots,
        final_answer_system_prompt="""
Tu es un assistant qui modifie des événements.
Tu as reçu le titre et les instructions.
""",
        on_ready=modify_agenda_on_ready,
    )

    email_summary_slots = [
        Slot(
            name="count",
            description="le nombre d'emails à résumer (par défaut 5)",
            question="Combien d'emails voulez-vous que je résume ?",
        )
    ]

    email_summary_skill = Skill(
        name="email_summary",
        description="faire une synthèse des derniers emails reçus",
        slots=email_summary_slots,
        final_answer_system_prompt="""
Tu es un assistant qui résume les emails.
""",
        on_ready=email_summary_on_ready,
    )

    music_slots = [
        Slot(
            name="music",
            description="le nom de la musique",
            question="Quelle est le nom de la musique",
        )
    ]

    music_skill = Skill(
        name="music",
        description="le nom de la musique",
        slots=music_slots,
        final_answer_system_prompt="""
Tu es un assistant en musique.
Tu reçois une données structurée, tu vas recevoir le nom de la musique.
exemple de phrase : "je veux ecouter get_back"
""",
        on_ready=music_on_ready,
    )

    write_file_slots = [
        Slot(
            name="name",
            description="le nom du fichier que je veux créer",
            question="Quelle est le nom du fichier",
        ),
        Slot(
            name="content",
            description="le contenu du fichier",
            question="Quelle est le contenu du fichier",
        )
    ]

    write_file_skill = Skill(
        name="file",
        description="crer le fichier txt avec le name et le content",
        slots=write_file_slots,
        final_answer_system_prompt="""
Tu es un assistant création de fichier.
Tu reçois des données structurées, tu vas recevoir le nom et le contenue du fichier.
tu devras alors créer ce fichier avec l'extension .txt, tu vas récupérer le nom du fichier et le contenu"
""",
        on_ready=write_txt_file_on_ready,
    )

    # Skill météo
    weather_slots = [
        Slot(
            name="city",
            description="la ville pour la météo (ex: Annecy, Paris, Lyon)",
            question="Pour quelle ville veux-tu la météo ?",
        ),
        Slot(
            name="date",
            description="la date pour la météo (ex: aujourd'hui, demain, 2025-12-15)",
            question="Pour quelle date veux-tu la météo ?",
        ),
    ]

    weather_skill = Skill(
        name="weather",
        description="questions à propos de la météo en fonction d'une ville et d'une date",
        slots=weather_slots,
        final_answer_system_prompt="""
Tu es un assistant météo.
Tu reçois des données structurées (ville, date, prévisions, etc.)
et tu dois formuler une réponse météo en français, concise et naturelle.
""",
        on_ready=weather_on_ready,
    )


    file_writer = Skill(
        name="write_txt_file",
        description="Ecrire du contenu dans un fichier texte",
        slots=[
            Slot(
                name="file_path",
                description="le chemin du fichier texte",
                question="Quel est le nom du fichier texte où écrire ?",
            ),
            Slot(
                name="content",
                description="le contenu du fichier texte",
                question="Quel est le contenu du fichier texte ?",
            )
        ],
        final_answer_system_prompt="""Tu es un assistant qui permet d'écrire du contenu dans un fichier texte. Tu dois créer ou écraser le fichier texte spécifié avec le contenu fourni.""",
        on_ready=write_txt_file_on_ready,
    )

    file_reader = Skill(
        name="read_txt_file",
        description="Lire du contenu dans un fichier texte",
        slots=[
            Slot(
                name="file_path",
                description="le chemin du fichier texte",
                question="Quel est le nom du fichier texte à lire ?",
            ),
        ],
        final_answer_system_prompt="""Tu es un assistant qui permet de lire du contenu dans un fichier texte. Tu dois lire le fichier texte spécifié et retourner son contenu.""",
        on_ready=read_txt_file_on_ready,
    )

    # Skill réservation de restaurant
    booking_slots = [
        Slot(
            name="restaurant_name",
            description="le nom du restaurant ou type de cuisine (ex: italien, japonais)",
            question="Dans quel restaurant ou quel type de cuisine veux-tu réserver ?",
        ),
        Slot(
            name="date",
            description="la date de la réservation",
            question="Pour quel jour veux-tu réserver ?",
        ),
        Slot(
            name="time",
            description="l'heure de la réservation",
            question="À quelle heure ?",
        ),
        Slot(
            name="people",
            description="le nombre de personnes",
            question="Pour combien de personnes ?",
        ),
    ]

    booking_skill = Skill(
        name="booking",
        description="organisation d'une réservation de restaurant",
        slots=booking_slots,
        final_answer_system_prompt="""
Tu es un assistant qui aide à réserver un restaurant.
Tu reçois soit des données structurées, soit un résumé, et tu dois
répondre en français en récapitulant clairement la réservation.
""",
        on_ready=booking_on_ready,
    )

    smalltalk_skill = Skill(
        name="smalltalk",
        description="conversation générale, questions diverses, discuter de tout et de rien",
        slots=[],
        final_answer_system_prompt="""
Tu es un assistant conversationnel général.
Réponds naturellement en français, de façon sympathique et concise.
""",
        on_ready=None,
    )

    return MultiSkillAgent([
        weather_skill, 
        booking_skill, 
        smalltalk_skill, 
        music_skill, 
        write_file_skill, 
        file_writer, 
        file_reader, 
        agenda_skills,
        delete_agenda_skill,
        modify_agenda_skill,
        email_summary_skill
    ])


# =========================
# Boucle principale
# =========================

def main():
    agent = build_agent()
    print("Assistant: Salut !")
    print("Tu peux me parler météo, réservation de resto, ou juste discuter.")
    print("Tape 'quit' pour arrêter, ou 'reset' pour annuler une demande en cours.\n")

    while True:
        user_msg = input("Utilisateur: ").strip()
        if not user_msg:
            continue
        if user_msg.lower() in {"quit", "exit"}:
            print("Assistant: À bientôt !")
            break

        try:
            answer = agent.handle_user_message(user_msg)
        except Exception as e:
            print("Erreur interne:", e)
            answer = "Oups, j'ai eu un souci interne, peux-tu réessayer ?"

        print("Assistant:", answer)


if __name__ == "__main__":
    main()