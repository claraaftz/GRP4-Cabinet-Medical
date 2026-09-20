from datetime import datetime
from models.patient import Patient
from utils.validators import InvalidConsultationStatusError
 
 
class Consultation:
    def __init__(self, date_heure: datetime, patient: Patient, nom_medecin: str, motif: str, statut: str = "planifiée"):
        self._date_heure = date_heure
        self._patient = patient
        self._nom_medecin = nom_medecin
        self._motif = motif
        self._diagnostic = ""
        self._prescriptions = []
 
        statuts_valides = ["planifiée", "réalisée", "annulée"]
        if statut not in statuts_valides:
            raise InvalidConsultationStatusError(f"Statut invalide : {statut}")
        self._statut = statut
 
 
    #---getters . setters
    @property
    def date_heure(self) -> datetime:
        return self._date_heure
 
    @property
    def patient(self) -> Patient:
        return self._patient
 
    @property
    def nom_medecin(self) -> str:
        return self._nom_medecin
 
    @property
    def motif(self) -> str:
        return self._motif
 
    @property
    def diagnostic(self) -> str:
        return self._diagnostic
 
    @property
    def prescriptions(self) -> list:
        return self._prescriptions
 
    @property
    def statut(self) -> str:
        return self._statut
 
 
   
    #-----contraintes consignes
    def modifier_date_heure(self, nouvelle_date_heure: datetime):
        if self.statut != "planifiée":
            raise InvalidConsultationStatusError("Impossible de modifier une consultation déjà réalisée ou annulée.")
        self._date_heure = nouvelle_date_heure
 
    def ajouter_diagnostic(self, diagnostic: str):
        if self.statut != "réalisée":
            raise InvalidConsultationStatusError("Le diagnostic ne peut être ajouté que si la consultation est réalisée.")
        self._diagnostic = diagnostic
 
    def ajouter_prescription(self, prescription):
        if self.statut != "réalisée":
            raise InvalidConsultationStatusError("Impossible d'ajouter une prescription à une consultation non réalisée.")
        self._prescriptions.append(prescription)
 
    def marquer_realisee(self):
        if self.statut == "annulée":
            raise InvalidConsultationStatusError("Impossible de réaliser une consultation annulée.")
        self._statut = "réalisée"
 
    def annuler(self):
        if self.statut == "réalisée":
            raise InvalidConsultationStatusError("Impossible d'annuler une consultation déjà réalisée.")
        self._statut = "annulée"
 
    @staticmethod
    def _prescription_to_dict(prescription) -> dict:
        details = {
            "type": type(prescription).__name__,
            "traitement": getattr(prescription, "_traitement", ""),
            "posologie": getattr(prescription, "_posologie", ""),
            "duree_traitement": getattr(prescription, "_duree_traitement", ""),
        }

        for attribut in (
            "_medicament",
            "_dosage",
            "_frequence",
            "_type_examen",
            "_laboratoire_recommande",
            "_zone_traite",
            "_nb_seance",
        ):
            if hasattr(prescription, attribut):
                details[attribut[1:]] = getattr(prescription, attribut)

        return details

    def to_dict(self) -> dict:
        return {
            "date_heure": self.date_heure.isoformat(),
            "patient_secu": self.patient.n_securite_sociale,
            "nom_medecin": self.nom_medecin,
            "motif": self.motif,
            "diagnostic": self.diagnostic,
            "statut": self.statut,
            "prescriptions": [self._prescription_to_dict(p) for p in self.prescriptions]
        }