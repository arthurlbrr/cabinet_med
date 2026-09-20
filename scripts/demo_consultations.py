from datetime import datetime, timedelta
from services import consultation_services as cs


def main():
    print("Demo: gestion des consultations")

    # préparer un patient factice (le patient doit exister dans data; si non, ajouter manuellement)
    sample_patient_id = "000000000000000"
    now = datetime.now()

    try:
        # planifier (va lever PatientNotFoundError si patient absent)
        c = cs.schedule_consultation(sample_patient_id, now + timedelta(days=1), "Dr Test", "Contrôle")
        print("Planifiée:", c)
    except Exception as e:
        print("Erreur planification (vérifier patient existant) :", e)

    # lister à venir
    upcoming = cs.get_upcoming_consultations()
    print("Consultations à venir:")
    for it in upcoming:
        print(" -", it)

    # si une consultation existe, la marquer réalisée et ajouter diagnostic + prescriptions
    if upcoming:
        cid = upcoming[0]["id"]
        try:
            cs.mark_consultation_realized(cid)
            print(f"Consultation {cid} marquée réalisée")
            cs.add_diagnostic(cid, "Diagnostic exemple")
            print(f"Diagnostic ajouté pour {cid}")
            cs.add_prescriptions(cid, ["Med A 10mg", "Med B 5mg"])
            print(f"Prescriptions ajoutées pour {cid}")
        except Exception as e:
            print("Erreur modification consultation:", e)


if __name__ == "__main__":
    main()
