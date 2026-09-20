from abc import ABC, abstractmethod


__all__ = [
    "PrescriptionMedicamenteuse",
    "PrescriptionExamen",
    "PrescriptionKinesitherapie"
]

class Prescription(ABC) :

    def __init__(self, traitement: str, posologie: str, duree_traitement: str ) -> None:
        self._traitement = traitement
        self._posologie = posologie
        self._duree_traitement = duree_traitement

    @abstractmethod
    def afficher_details(self) :
        pass


class PrescriptionMedicamenteuse(Prescription) :

    def __init__(self, medicament: str, posologie: str, duree_traitement: str, dosage: str, frequence: str) -> None:
        super().__init__(medicament, posologie, duree_traitement)
        self._medicament = medicament
        self._dosage = dosage
        self._frequence = frequence

    @property
    def afficher_details(self) -> str:
        return (
            "Prescription medicamenteuse :\n"
            f"- Medicament : {self._medicament}\n"
            f"- Dosage : {self._dosage}\n"
            f"- Fréquence : {self._frequence}\n"
            f"- Posologie : {self._posologie}\n"
            f"- Durée du traitement : {self._duree_traitement}\n"
            )
    
class PrescriptionExamen(Prescription):

    def __init__(self, type_examen: str, laboratoire_recommande: str, *, posologie: str ="Aucune", duree_traitement: str ="Aucune", ) -> None:
        super().__init__(type_examen, posologie, duree_traitement)
        self._type_examen = type_examen
        self._laboratoire_recommande = laboratoire_recommande

    @property
    def afficher_details(self) -> str:
        return (
            "Prescription d'examen :\n"
            f"- Type d'examen : {self._type_examen}\n"
            f"- laboratoire recommandé : {self._laboratoire_recommande}\n"
            f"- Posologie : {self._posologie}\n"
            f"- Durée du traitement : {self._duree_traitement}\n"
        )

class PrescriptionKinesitherapie(Prescription) :

    def __init__(self, zone_traite, nb_seance, posologie="À définir", duree_traitement="À définir"):
        super().__init__("Kinesitherapie", posologie, duree_traitement)
        self._zone_traite = zone_traite
        self._nb_seance = nb_seance

    @property   
    def afficher_details(self) -> str:
        return (
            "Prescription Kinesitherapie \n"
            f"- Zone à traité : {self._zone_traite} \n"
            f"- Nombre de seance : {self._nb_seance} \n"
            f"- Posologie : {self._posologie}\n"
            f"- Durée du traitement : {self._duree_traitement}\n"
        )

    


