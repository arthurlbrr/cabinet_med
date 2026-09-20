"""Fonctions de validation simples (niveau débutant)."""
from typing import Union


def validate_ssn(ssn: Union[str, int]) -> bool:
    """Valide un numéro de sécurité sociale simple : 15 chiffres.

    Retourne True si c'est bon, False sinon.
    """
    s = str(ssn).strip()
    return s.isdigit() and len(s) == 15
