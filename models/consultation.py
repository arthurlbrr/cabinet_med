from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ConsultationStatus(Enum):
    PLANIFIEE = "planifiée"
    REALISEE = "réalisée"
    ANNULEE = "annulée"


@dataclass
class Consultation:
    id: int
    date_time: datetime
    patient: Any  # stocker id du patient pour la persistance
    practitioner: str
    reason: str
    diagnostic: Optional[str] = None
    prescriptions: List[str] = field(default_factory=list)
    status: ConsultationStatus = ConsultationStatus.PLANIFIEE

    def can_modify(self) -> bool:
        return self.status == ConsultationStatus.PLANIFIEE

    def update(self, *, date_time: Optional[datetime] = None, practitioner: Optional[str] = None, reason: Optional[str] = None) -> None:
        if not self.can_modify():
            raise ValueError("Impossible de modifier : le statut ne le permet pas.")
        if date_time is not None:
            self.date_time = date_time
        if practitioner is not None:
            self.practitioner = practitioner
        if reason is not None:
            self.reason = reason

    def set_status(self, new_status: ConsultationStatus) -> None:
        if not isinstance(new_status, ConsultationStatus):
            raise ValueError("Statut invalide")
        self.status = new_status

    def set_diagnostic(self, text: str) -> None:
        if self.status != ConsultationStatus.REALISEE:
            raise ValueError("Le diagnostic ne peut être ajouté que si la consultation est réalisée.")
        self.diagnostic = text

    def add_prescription(self, prescription: str) -> None:
        self.prescriptions.append(prescription)

    def add_prescriptions(self, prescriptions: List[str]) -> None:
        self.prescriptions.extend(prescriptions)

    def remove_prescription(self, prescription: str) -> None:
        try:
            self.prescriptions.remove(prescription)
        except ValueError:
            raise ValueError("Prescription non trouvée")

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["date_time"] = self.date_time.isoformat()
        d["status"] = self.status.value
        return d

    @classmethod
    def from_dict(cls, data: Dict) -> "Consultation":
        return cls(
            id=int(data["id"]),
            date_time=datetime.fromisoformat(data["date_time"]),
            patient=data["patient"],
            practitioner=data["practitioner"],
            reason=data["reason"],
            diagnostic=data.get("diagnostic"),
            prescriptions=data.get("prescriptions", []),
            status=ConsultationStatus(data.get("status", ConsultationStatus.PLANIFIEE.value)),
        )
