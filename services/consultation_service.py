from datetime import datetime
from models.consultation import Consultation
from models.prescription import Prescription
from utils.decorators import log_action, validate_patient
from utils.validators import ConsultationNotFoundError
 
 
class ConsultationService:
    def __init__(self, patient_service = None,consultations: list = None):
        self.patient_service = patient_service
        #recup dictionnaire patients OU en créer un vide
        self.patients = (patient_service.patients if patient_service is not None else {})
        self.consultations = consultations if consultations is not None else []
 
    #Méthode : planifier une consultation
    @log_action("Planification d'une consultation")
    @validate_patient
    def planifier_consultation(self, n_securite_sociale: str, date_heure: datetime, nom_medecin: str, motif: str) -> Consultation:
        patient = self.patients[n_securite_sociale]
 
        consultation = Consultation(date_heure=date_heure, patient=patient, nom_medecin=nom_medecin, motif=motif, statut="planifiée")
        self.consultations.append(consultation)
        patient.liste_consultations.append(consultation)
        return consultation
 
    #Méthode : afficher les consultations à venir
    @log_action("Affichage liste des consultations à venir")
    def afficher_consultations_a_venir(self):
        maintenant = datetime.now()
        a_venir = [c for c in self.consultations if c.date_heure >= maintenant and c.statut == "planifiée"]
        if not a_venir:
            print("Aucune consultation à venir.")
            return
        print("\n--- Consultations à venir ---")
 
        for i in a_venir:
            print(f"{i.date_heure.strftime('%Y-%m-%d %H:%M')} - Patient : {i.patient.nom} {i.patient.prenom} - Dr. {i.nom_medecin} - Motif : {i.motif}")
 
    #Méthode : changer le statut de la consultation
    @log_action("Changement de statut : Consultation réalisée")
    def marquer_realisee(self, consultation: Consultation):
        consultation.marquer_realisee()
 
    #Méthode : annuler la consultation
    @log_action("Annulation de consultation")
    def annuler_consultation(self, consultation: Consultation):
        consultation.annuler()
 
    #Méthode : ajouter un diagnostic
    @log_action("Ajout d'un diagnostic")
    def ajouter_diagnostic(self, consultation: Consultation, diagnostic: str):
        consultation.ajouter_diagnostic(diagnostic)
 
    #Méthode : ajouter une prescription
    @log_action("Ajout de prescription(s)")
    def ajouter_prescriptions(self, consultation: Consultation, *prescriptions: Prescription):
        for prescription in prescriptions:
            consultation.ajouter_prescription(prescription)