import requests
from typing import List, Dict, Optional

LLAMA_SERVER_URL = "http://localhost:8080/v1/chat/completions"
MODEL_NAME = "Qwen_Qwen3-0.6B-Q8_0"


def send_llama_chat(
    user_content: str,
    system_prompt: str = "You are a helpful assistant.",
    history: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0,
    max_tokens: int = 512,
) -> str:
    """
    Envoie une requête de type chat à llama-server avec un system prompt.
    
    :param user_content: Le message utilisateur actuel.
    :param system_prompt: Le prompt système (rôle / comportement du modèle).
    :param history: Historique de la conversation, liste de dicts:
                    [{"role": "user"/"assistant", "content": "..."}, ...]
    :param temperature: Température du modèle.
    :param max_tokens: Nombre max de tokens générés.
    :return: La réponse texte du modèle.
    """
    if history is None:
        history = []

    # Construction de la liste des messages pour un endpoint style OpenAI
    messages = [
        {"role": "system", "content": system_prompt},
        *history,
        {"role": "user", "content": user_content},
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        # tu peux ajouter d'autres paramètres supportés par ton serveur:
        # "top_p": 0.95,
        # "stream": False,
    }

    try:
        response = requests.post(LLAMA_SERVER_URL, json=payload, timeout=60)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur lors de l'appel à llama-server: {e}") from e

    data = response.json()

    # Pour une API type OpenAI, la réponse est souvent dans:
    # data["choices"][0]["message"]["content"]
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Format de réponse inattendu: {data}") from e


if __name__ == "__main__":
    # Exemple d'utilisation
    system_prompt = (
        "Tu es un assistant spécialisé en développement Python. "
        "Réponds en français, de manière concise et claire."
    )

    # Historique fictif
    history = [
        {"role": "user", "content": "Salut, qui es-tu ?"},
        {"role": "assistant", "content": "Je suis un modèle de langage basé sur Qwen."},
    ]

    question = "Peux-tu m'expliquer ce qu'est un décorateur en Python ?"

    answer = send_llama_chat(
        user_content=question,
        system_prompt=system_prompt,
        history=history,
    )

    print("Réponse du modèle :")
    print(answer)