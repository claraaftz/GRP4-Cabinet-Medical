from models.patient import Patient
from utils.decorators import log_action, validate_patient
from utils.validators import PatientNotFoundError
 
 
class PatientService:
    def __init__(self, patients: dict = None):
        self.patients = patients if patients is not None else {} #permet d'avoir un dictionnaire neuf a chaque utilisation
 
    @log_action("Ajout d'un patient")
    def ajouter_patient(self, patient: Patient):
        if patient.n_securite_sociale in self.patients:
            raise ValueError("Ce numéro de sécurité sociale existe déjà.")
        self.patients[patient.n_securite_sociale] = patient
 
 
    @validate_patient
    def rechercher_patient(self, numero_securite_sociale: str) -> Patient:
        return self.patients[numero_securite_sociale]
 
 
    @log_action("Affichage liste des patients")
    def afficher_liste_patients(self):
        if not self.patients:
            print("Aucun patient enregistré.")
            return
        for p in self.patients.values():
            print(f"{p.n_securite_sociale} - {p.nom} {p.prenom} | Âge : {p.age} ans | Tél : {p.telephone}")
 
 
   
    @log_action("Consultation de l'historique patient")
    @validate_patient
    def afficher_historique_patient(self, numero_securite_sociale: str):
        patient = self.patients[numero_securite_sociale]
        if not patient.liste_consultations:
            print(f"Aucune consultation pour {patient.nom} {patient.prenom}.")
            return
 
        print(f"\nHistorique de {patient.nom} {patient.prenom} :")
        for c in patient.liste_consultations:
            print(f"- {c.date_heure.strftime('%Y-%m-%d %H:%M')} | Dr. {c.nom_medecin} | Motif: {c.motif} | Statut: {c.statut}")
            if c.diagnostic:
                print(f"  Diagnostic : {c.diagnostic}")
            for pres in c.prescriptions:
                print(f"  Ord : {pres.afficher_details()}")
 
