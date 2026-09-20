import json
import os
from datetime import datetime, date
from models.patient import Patient
from models.consultation import Consultation
from models.prescription import (Prescription, PrescriptionMedicamenteuse, PrescriptionExamen, PrescriptionKinesitherapie)
from services.patient_service import PatientService
from services.consultation_service import ConsultationService
from utils.validators import (PatientNotFoundError, InvalidSecurityNumberError, InvalidConsultationStatusError, ConsultationNotFoundError)

DATA_FILE = "data/cabinet_data.json"


def sauvegarder_donnees(patient_service: PatientService, consultation_service: ConsultationService):
    os.makedirs("data", exist_ok=True)
    data = {
        "patients": [p.to_dict() for p in patient_service.patients.values()],
        "consultations": [c.to_dict() for c in consultation_service.consultations]
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def charger_donnees(patient_service: PatientService, consultation_service: ConsultationService):
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Reconstitution des patients
    for p_data in data.get("patients", []):
        patient = Patient(
            n_securite_sociale=p_data["n_securite_sociale"],
            nom=p_data["nom"],
            prenom=p_data["prenom"],
            date_naissance=date.fromisoformat(p_data["date_naissance"]),
            adresse=p_data["adresse"],
            telephone=p_data["telephone"]
        )
        patient_service.patients[patient.n_securite_sociale] = patient

    # 2. Reconstitution des consultations
    for c_data in data.get("consultations", []):
        patient = patient_service.patients.get(c_data["patient_secu"])
        if not patient:
            continue

        consultation = Consultation(
            date_heure=datetime.fromisoformat(c_data["date_heure"]),
            patient=patient,
            nom_medecin=c_data["nom_medecin"],
            motif=c_data["motif"],
            statut=c_data["statut"]
        )
        if c_data.get("diagnostic"):
            consultation._diagnostic = c_data["diagnostic"]

        for pres_data in c_data.get("prescriptions", []):
            prescription = Prescription.from_dict(pres_data)
            consultation.prescriptions.append(prescription)

        consultation_service.consultations.append(consultation)
        patient.liste_consultations.append(consultation)


def afficher_menu():
    print("\n" + "=" * 45)
    print("    GESTION DU CABINET MÉDICAL")
    print("=" * 45)
    print("--- PATIENTS ---")
    print("1. Ajouter un patient")
    print("2. Rechercher un patient")
    print("3. Afficher tous les patients")
    print("4. Historique d'un patient")
    print("--- CONSULTATIONS ---")
    print("5. Planifier une consultation")
    print("6. Afficher les consultations à venir")
    print("7. Marquer une consultation comme réalisée")
    print("8. Annuler une consultation")
    print("9. Ajouter un diagnostic à une consultation")
    print("10. Ajouter une prescription à une consultation")
    print("--- SYSTÈME ---")
    print("0. Quitter")
    print("=" * 45)


def saisir_index_consultation(patient: Patient) -> Consultation:
    """Utilitaire pour afficher et vérifier la sélection d'une consultation."""
    if not patient.liste_consultations:
        raise ConsultationNotFoundError("Aucune consultation enregistrée pour ce patient.")

    print("\nConsultations du patient :")
    for i, c in enumerate(patient.liste_consultations):
        print(f"[{i}] {c.date_heure.strftime('%Y-%m-%d %H:%M')} - Statut : {c.statut}")

    saisie = input("Sélectionner l'index de la consultation : ").strip()
    if not saisie.isdigit():
        raise ValueError("L'index doit être un nombre entier valide.")

    idx = int(saisie)
    if idx < 0 or idx >= len(patient.liste_consultations):
        raise IndexError("Index de consultation hors de la liste.")

    return patient.liste_consultations[idx]


def main():
    patient_service = PatientService()
    consultation_service = ConsultationService(patient_service=patient_service)

    # Chargement des données au démarrage
    charger_donnees(patient_service, consultation_service)

    def auto_save():
        sauvegarder_donnees(patient_service, consultation_service)

    while True:
        afficher_menu()
        choix = input("Choisissez une option : ").strip()

        try:
            if choix == "1":
                secu = input("Numéro de sécurité sociale (15 chiffres) : ").strip()
                nom = input("Nom : ").strip()
                prenom = input("Prénom : ").strip()
                date_str = input("Date de naissance (AAAA-MM-JJ) : ").strip()
                adresse = input("Adresse : ").strip()
                tel = input("Téléphone : ").strip()

                dt_naissance = date.fromisoformat(date_str)
                p = Patient(secu, nom, prenom, dt_naissance, adresse, tel)
                patient_service.ajouter_patient(p)
                auto_save()
                print("\n Patient ajouté avec succès !")

            elif choix == "2":
                secu = input("Numéro de sécurité sociale : ").strip()
                p = patient_service.rechercher_patient(secu)
                print(f"\n[Trouvé] {p}")

            elif choix == "3":
                patient_service.afficher_liste_patients()

            elif choix == "4":
                secu = input("Numéro de sécurité sociale du patient : ").strip()
                patient_service.afficher_historique_patient(secu)

            elif choix == "5":
                secu = input("Numéro de sécurité sociale du patient : ").strip()
                dt_str = input("Date et heure (AAAA-MM-JJ HH:MM) : ").strip()
                medecin = input("Nom du médecin : ").strip()
                motif = input("Motif : ").strip()

                dt_consultation = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                consultation_service.planifier_consultation(secu, dt_consultation, medecin, motif)
                auto_save()
                print("\n Consultation planifiée avec succès !")

            elif choix == "6":
                consultation_service.afficher_consultations_a_venir()

            elif choix == "7":
                secu = input("N° Sécurité sociale du patient : ").strip()
                p = patient_service.rechercher_patient(secu)
                c = saisir_index_consultation(p)

                consultation_service.marquer_realisee(c)
                auto_save()
                print("\n Consultation marquée comme réalisée !")

            elif choix == "8":
                secu = input("N° Sécurité sociale du patient : ").strip()
                p = patient_service.rechercher_patient(secu)
                c = saisir_index_consultation(p)

                consultation_service.annuler_consultation(c)
                auto_save()
                print("\n Consultation annulée !")

            elif choix == "9":
                secu = input("N° Sécurité sociale du patient : ").strip()
                p = patient_service.rechercher_patient(secu)
                c = saisir_index_consultation(p)
                diag = input("Diagnostic : ").strip()

                consultation_service.ajouter_diagnostic(c, diag)
                auto_save()
                print("\n Diagnostic ajouté !")

            elif choix == "10":
                secu = input("N° Sécurité sociale du patient : ").strip()
                p = patient_service.rechercher_patient(secu)
                c = saisir_index_consultation(p)

                print("\nType de prescription : 1. Médicamenteuse | 2. Examen | 3. Kinésithérapie")
                t = input("Choix : ").strip()
                if t == "1":
                    med = input("Médicament : ").strip()
                    dos = input("Dosage : ").strip()
                    freq = input("Fréquence : ").strip()
                    poso = input("Posologie : ").strip()
                    duree = input("Durée : ").strip()
                    pres = PrescriptionMedicamenteuse(med, poso, duree, dos, freq)
                elif t == "2":
                    exam = input("Type d'examen : ").strip()
                    labo = input("Laboratoire : ").strip()
                    pres = PrescriptionExamen(exam, labo)
                elif t == "3":
                    zone = input("Zone à traiter : ").strip()
                    nb_str = input("Nombre de séances : ").strip()
                    if not nb_str.isdigit():
                        raise ValueError("Le nombre de séances doit être un chiffre.")
                    pres = PrescriptionKinesitherapie(zone, int(nb_str))
                else:
                    print("\n Type de prescription invalide.")
                    continue

                consultation_service.ajouter_prescriptions(c, pres)
                auto_save()
                print("\n Prescription ajoutée !")

            elif choix == "0":
                print("\nAu revoir !")
                break

            else:
                print("\n Option invalide. Veuillez réessayer.")

        except (
            PatientNotFoundError,
            InvalidSecurityNumberError,
            InvalidConsultationStatusError,
            ConsultationNotFoundError,
            ValueError,
            IndexError
        ) as e:
            print(f"\n Erreur : {e}")


if __name__ == "__main__":
    main()