from __future__ import annotations
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


# Exceptions spécifiques
class PatientNotFoundError(Exception):
	pass


class ConsultationNotFoundError(Exception):
	pass


class InvalidConsultationStatusError(Exception):
	pass


_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cabinet_data.json")


def _load_data() -> Dict:
	if not os.path.exists(_DATA_PATH):
		return {"patients": [], "consultations": []}
	try:
		with open(_DATA_PATH, "r", encoding="utf-8") as f:
			content = f.read().strip()
			if not content:
				return {"patients": [], "consultations": []}
			return json.loads(content)
	except (json.JSONDecodeError, FileNotFoundError):
		return {"patients": [], "consultations": []}


def _save_data(data: Dict) -> None:
	os.makedirs(os.path.dirname(_DATA_PATH), exist_ok=True)
	with open(_DATA_PATH, "w", encoding="utf-8") as f:
		json.dump(data, f, indent=2, ensure_ascii=False)


def _next_consultation_id(data: Dict) -> int:
	cons = data.get("consultations", [])
	if not cons:
		return 1
	try:
		return max(int(c.get("id", 0)) for c in cons) + 1
	except Exception:
		return len(cons) + 1


def _find_patient(data: Dict, patient_id: str) -> Optional[Dict]:
	for p in data.get("patients", []):
		# accepter plusieurs champs possibles (ssn, id, security_number)
		if any(str(p.get(k)) == str(patient_id) for k in ("ssn", "id", "security_number", "numero_secu")):
			return p
	return None


def _find_consultation_index(data: Dict, consultation_id: int) -> int:
	for i, c in enumerate(data.get("consultations", [])):
		try:
			if int(c.get("id")) == int(consultation_id):
				return i
		except Exception:
			continue
	return -1


def schedule_consultation(patient_id: str, date_time: datetime, practitioner: str, reason: str) -> Dict:
	"""Crée et persiste une nouvelle consultation (status = 'planifiée').

	Lève PatientNotFoundError si le patient n'existe pas dans le JSON.
	Retourne le dict de la consultation créée.
	"""
	data = _load_data()
	if _find_patient(data, patient_id) is None:
		raise PatientNotFoundError(f"Patient {patient_id} non trouvé.")

	new_id = _next_consultation_id(data)
	consult = {
		"id": new_id,
		"date_time": date_time.isoformat(),
		"patient": str(patient_id),
		"practitioner": practitioner,
		"reason": reason,
		"diagnostic": None,
		"prescriptions": [],
		"status": "planifiée",
	}
	data.setdefault("consultations", []).append(consult)
	_save_data(data)
	return consult


def get_upcoming_consultations(now: Optional[datetime] = None) -> List[Dict]:
	"""Retourne consultations planifiées dont date_time >= now triées par date_time."""
	if now is None:
		now = datetime.now()
	data = _load_data()
	out = []
	for c in data.get("consultations", []):
		try:
			c_dt = datetime.fromisoformat(c.get("date_time"))
		except Exception:
			continue
		if c.get("status") == "planifiée" and c_dt >= now:
			out.append(c)
	out.sort(key=lambda x: x.get("date_time"))
	return out


def mark_consultation_realized(consultation_id: int) -> Dict:
	data = _load_data()
	idx = _find_consultation_index(data, consultation_id)
	if idx == -1:
		raise ConsultationNotFoundError(f"Consultation {consultation_id} non trouvée.")
	data["consultations"][idx]["status"] = "réalisée"
	_save_data(data)
	return data["consultations"][idx]


def cancel_consultation(consultation_id: int) -> Dict:
	data = _load_data()
	idx = _find_consultation_index(data, consultation_id)
	if idx == -1:
		raise ConsultationNotFoundError(f"Consultation {consultation_id} non trouvée.")
	data["consultations"][idx]["status"] = "annulée"
	_save_data(data)
	return data["consultations"][idx]


def add_diagnostic(consultation_id: int, text: str) -> Dict:
	data = _load_data()
	idx = _find_consultation_index(data, consultation_id)
	if idx == -1:
		raise ConsultationNotFoundError(f"Consultation {consultation_id} non trouvée.")
	consult = data["consultations"][idx]
	if consult.get("status") != "réalisée":
		raise InvalidConsultationStatusError("Le diagnostic ne peut être ajouté que si la consultation est réalisée.")
	consult["diagnostic"] = text
	_save_data(data)
	return consult


def add_prescriptions(consultation_id: int, prescriptions: List[str]) -> Dict:
	data = _load_data()
	idx = _find_consultation_index(data, consultation_id)
	if idx == -1:
		raise ConsultationNotFoundError(f"Consultation {consultation_id} non trouvée.")
	consult = data["consultations"][idx]
	consult.setdefault("prescriptions", []).extend(prescriptions)
	_save_data(data)
	return consult


def get_consultation(consultation_id: int) -> Dict:
	data = _load_data()
	idx = _find_consultation_index(data, consultation_id)
	if idx == -1:
		raise ConsultationNotFoundError(f"Consultation {consultation_id} non trouvée.")
	return data["consultations"][idx]

