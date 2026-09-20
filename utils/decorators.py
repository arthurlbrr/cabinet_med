"""Décorateurs légers et lisibles.

Contenu :
- `log_action`: log simple dans `logs.txt` (ne fait pas planter l'app en cas d'erreur de log)
- `validate_patient`: vérifie qu'un patient existe dans le JSON avant d'exécuter la fonction
"""
from functools import wraps
from datetime import datetime
import os
import json

from .exceptions import PatientNotFoundError


# Chemins simples basés sur le dossier parent du module
ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_PATH = os.path.join(ROOT, "logs.txt")
DATA_PATH = os.path.join(ROOT, "data", "cabinet_data.json")

# Clés possibles pour identifier un patient dans le JSON
PATIENT_KEYS = ("ssn", "id", "security_number", "numero_secu")


def _load_data():
    """Charge le JSON du cabinet; retourne {'patients': []} en cas d'erreur."""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"patients": []}


def log_action(action_desc):
    """Décorateur simple qui ajoute une ligne dans `logs.txt`.

    L'application continue même si l'écriture échoue.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            line = f"[{datetime.now().isoformat()}] {action_desc}\n"
            try:
                with open(LOG_PATH, "a", encoding="utf-8") as f:
                    f.write(line)
            except Exception:
                # Ne pas interrompre l'exécution pour un problème de log
                pass
            return result

        return wrapper

    return decorator


def validate_patient(arg_name="patient_id"):
    """Vérifie que le patient existe avant d'appeler la fonction.

    Récupère l'argument par `kwargs` puis par position (premier argument).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if arg_name in kwargs:
                pid = kwargs[arg_name]
            elif args:
                pid = args[0]
            else:
                pid = None

            data = _load_data()

            for p in data.get("patients", []):
                for key in PATIENT_KEYS:
                    if str(p.get(key)) == str(pid):
                        return func(*args, **kwargs)

            raise PatientNotFoundError(f"Patient {pid} non trouvé.")

        return wrapper

    return decorator
