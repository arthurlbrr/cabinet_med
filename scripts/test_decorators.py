import json
from utils.exceptions import PatientNotFoundError
from utils.decorators import log_action, validate_patient

DATA_PATH = "data/cabinet_data.json"

@validate_patient()
def greet(patient_id):
    print(f"OK pour patient {patient_id}")


if __name__ == "__main__":
    print("--- Test 1: patient absent (devrait lever PatientNotFoundError) ---")
    try:
        greet("123")
    except PatientNotFoundError as e:
        print("Erreur attendue:", e)

    print("\n--- Test 2: ajouter patient '123' et réessayer ---")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # sauvegarder l'état initial
    original = json.dumps(data, indent=2, ensure_ascii=False)

    # ajouter un patient simple
    data.setdefault("patients", []).append({"id": "123", "name": "Test User"})
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    try:
        greet("123")
    except Exception as e:
        print("Erreur inattendue:", e)

    # restaurer l'état initial
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        f.write(original)

    print("\nTest terminé.")
