from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict


class Prescription(ABC):
    """Classe abstraite simple pour une prescription."""

    @abstractmethod
    def afficher_details(self) -> str:
        pass


@dataclass
class PrescriptionMedicamenteuse(Prescription):
    medicament: str
    dosage: str
    frequence: str

    def afficher_details(self) -> str:
        return f"Médicament: {self.medicament}, dosage: {self.dosage}, fréquence: {self.frequence}"


@dataclass
class PrescriptionExamen(Prescription):
    examen_type: str
    laboratoire: str

    def afficher_details(self) -> str:
        return f"Examen: {self.examen_type}, laboratoire recommandé: {self.laboratoire}"


@dataclass
class PrescriptionKinesitherapie(Prescription):
    seances: int
    zone: str

    def afficher_details(self) -> str:
        return f"Kiné: {self.seances} séances, zone: {self.zone}"
